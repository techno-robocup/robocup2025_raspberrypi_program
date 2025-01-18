#include <iostream>
#include <wiringPiI2C.h>
#include <unistd.h>

#define I2C_ADDRESS 0x08

int main()
{
    int fd = wiringPiI2CSetup(I2C_ADDRESS);
    if (fd == -1)
    {
        std::cerr << "Failed to open I2C device" << std::endl;
        return -1;
    }

    while (true)
    {
        int data = wiringPiI2CReadReg8(fd, 0);
        if (data == -1)
        {
            std::cerr << "error reading data" << std::endl;
        }
        else
        {
            std::cout << data << std::endl;
        }

        sleep(1);
    }

    return 0;
}
