@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"

rem Check if a Conan profile exists
set "PROFILE_EXISTS="
2>nul conan profile show && set "PROFILE_EXISTS=1"

if not defined PROFILE_EXISTS (
    rem If no profile exists, detect and create one
    echo No profile exists, creating one with 'conan profile detect'
    conan profile detect
)

conan create "%SCRIPT_DIR%\kit_sdk" --build=missing
conan create "%SCRIPT_DIR%\nv_usd" --build=missing
conan create "%SCRIPT_DIR%\carb_sdk" --build=missing
rem packman-provided pybind11 is already configured with wrong paths, use a
rem from-source one so that we don't insert wrong paths
rem conan create "%SCRIPT_DIR%\pybind11" --build=missing
conan create "%SCRIPT_DIR%\python" --build=missing

echo [DONE] all conan dependencies have been created
