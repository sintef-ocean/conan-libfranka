from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import (
    apply_conandata_patches, copy, export_conandata_patches, get, rmdir)
from conan.tools.microsoft import is_msvc
from conan.tools.env import Environment
from conan.tools.scm import Version
from os.path import join

required_conan_version = ">=2.0.0"


class PackageConan(ConanFile):
    name = "libfranka"
    description = "C++ library for Franka research robots"
    license = "Apache-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/frankaemika/libfranka"
    topics = ("franka", "robot")
    package_type = "shared-library"
    settings = "os", "arch", "compiler", "build_type"

    @property
    def _build_testing(self):
        return not self.conf.get("tools.build:skip_test",
                                 default=True, check_type=bool)

    @property
    def _min_cppstd(self):
        return 14

    @property
    def _compilers_minimum_version(self):
        return {
            "apple-clang": "10",
            "clang": "7",
            "gcc": "7",
            "msvc": "191",
        }

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires(f"libfranka-common/{self.conan_data['dependencies'][self.version]['libfranka-common']}@sintef/stable")
        self.requires("eigen/3.4.0")
        self.requires(f"poco/{self.conan_data['dependencies'][self.version]['poco']}")

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, self._min_cppstd)
        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if minimum_version and Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration(
                f"{self.ref} requires C++{self._min_cppstd}, which your compiler does not support."
            )
        if is_msvc(self) and self.options.shared:
            raise ConanInvalidConfiguration(f"{self.ref} can not be built as shared on Visual Studio and msvc.")

    def build_requirements(self):
        if self._build_testing:
            self.test_requires(f"gtest/{self.conan_data['dependencies'][self.version]['gtest']}")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_TESTS"] = self._build_testing
        tc.variables["BUILD_EXAMPLES"] = False
        tc.cache_variables["CMAKE_POLICY_DEFAULT_CMP0077"] = "NEW"
        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

        if self._build_testing:
            env = Environment()
            env.define("CTEST_OUTPUT_ON_FAILURE", "ON")
            with env.vars(self).apply():
                cmake.test()

    def package(self):
        copy(self, "LICENSE", self.source_folder, join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.libs = ["franka"]

        self.cpp_info.set_property("cmake_file_name", "Franka")
        self.cpp_info.set_property("cmake_target_name", "Franka::Franka")

        # Maybe need to set these INTERFACE_COMPILE_FEATURES:
        # cxx_attribute_deprecated;cxx_constexpr;cxx_defaulted_functions;
        # cxx_deleted_functions;cxx_generalized_initializers;cxx_noexcept;cxx_uniform_initialization

        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("m")
            self.cpp_info.system_libs.append("pthread")
            self.cpp_info.system_libs.append("dl")
