#include <Windows.h>
#include <d3d9.h>
#include <imgui.h>
#include <imgui_impl_dx9.h>
#include <imgui_impl_win32.h>
#include "MinHook.h"

// DirectX function prototypes
typedef HRESULT(__stdcall* EndScene)(LPDIRECT3DDEVICE9 pDevice);
EndScene oEndScene = nullptr;

HRESULT __stdcall hkEndScene(LPDIRECT3DDEVICE9 pDevice) {
    static bool initialized = false;
    if (!initialized) {
        ImGui::CreateContext();
        ImGui_ImplWin32_Init(FindWindow(NULL, L"oxyum internal cheat template"));
        ImGui_ImplDX9_Init(pDevice);
        initialized = true;
    }

    ImGui_ImplDX9_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();

    // Our GUI
    ImGui::Begin("oxyum intern temp");
    ImGui::Text("oxyum internal injection menu template : Version: 1.0.0");
    ImGui::End();

    ImGui::EndFrame();
    ImGui::Render();
    ImGui_ImplDX9_RenderDrawData(ImGui::GetDrawData());

    return oEndScene(pDevice);
}

// Hook initialization
DWORD WINAPI MainThread(LPVOID param) {
    if (MH_Initialize() != MH_OK) return 1;

    // Hook DirectX EndScene
    uintptr_t* vTable = *(uintptr_t**)GetModuleHandle(L"d3d9.dll"); // Simplified vtable lookup
    if (MH_CreateHook((LPVOID)vTable[42], &hkEndScene, reinterpret_cast<LPVOID*>(&oEndScene)) != MH_OK) return 1;
    MH_EnableHook(MH_ALL_HOOKS);
    return 0;
}

// DLL entry
BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) {
        DisableThreadLibraryCalls(hModule);
        CreateThread(NULL, 0, MainThread, hModule, 0, NULL);
    }
    return TRUE;
}