#include <cstdlib>
#include <iostream>

#include "franka/exception.h"
#include "franka/robot.h"

int main(void) {

  try {
    franka::Robot("localhost");

  } catch(const franka::NetworkException&) {
  }

  return EXIT_SUCCESS;
}
