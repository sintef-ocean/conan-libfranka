[![Linux GCC](https://github.com/sintef-ocean/conan-libfranka/workflows/Linux%20GCC/badge.svg)](https://github.com/sintef-ocean/conan-libfranka/actions?query=workflow%3A"Linux+GCC")

[Conan.io](https://conan.io) recipe for [libfranka](https://github.com/frankaemika/libfranka).

## How to use this package

1. Add remote to conan's package [remotes](https://docs.conan.io/2/reference/commands/remote.html)

   ```bash
   $ conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local
   ```

2. Using [*conanfile.txt*](https://docs.conan.io/2/reference/conanfile_txt.html) and *cmake* in your project.

   Add *conanfile.txt*:
   ```
   [requires]
   libfranka/<version>@sintef/stable

   [tool_requires]
   cmake/[>=3.25.0]

   [options]

   [layout]
   cmake_layout

   [generators]
   CMakeDeps
   CMakeToolchain
   VirtualBuildEnv
   ```
   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.13)
   project(TheProject CXX)

   find_package(Franka CONFIG REQUIRED)

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor Franka::Franka)
   ```
   Install and build e.g. a Release configuration:
   ```bash
   $ conan install . -s build_type=Release -pr:b=default
   $ source build/Release/generators/conanbuild.sh
   $ cmake --preset conan-release
   $ cmake --build build/Release
   $ source build/Release/generators/deactivate_conanbuild.sh
   ```

## Package options


## Known recipe issues
