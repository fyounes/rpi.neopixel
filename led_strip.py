#!/usr/bin/python3
# Author: Federico Younes
import time
import random

from neopixel import *

# LED strip configuration:
LED_COUNT = 60  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 150  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)


class FixedColorStrategy(object):
    """
    Fixed color for the whole range of pixels
    """

    def __init__(self, color):
        self.color = color

    def get_color(self, pixel):
        return self.color


class RandomColorStrategy(object):
    """
    Fixed color for the whole range of pixels. The color changes each it goes through pixel zero
    """

    def __init__(self):
        self.color = None

    def get_color(self, pixel):
        if self.color is None or pixel == 0:
            self.color = Color(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
        return self.color


class RainbowColorStrategy(object):
    """
    Colors range from blue to red. The colors returned are shifted with consecutive calls.
    """

    def __init__(self, rainbow_length=LED_COUNT):
        """
        :param rainbow_length: controls the pixel length of the the rainbow. This can determine whether the rainbow will
         fit entirely in the strip, loop around, etc
        """
        self.call_count = 0
        self.rainbow_length = rainbow_length

    def get_color(self, pixel):
        color = self.pick_color(pixel)
        if pixel == 0:
            self.call_count += 1
        if self.call_count == 255:
            # Prevent overflow if the rainbow runs for a while
            self.call_count = 0
        return color

    def pick_color(self, pixel):
        """
        Generate rainbow colors across 0-255 positions
        """
        pos = int(pixel * 256 / self.rainbow_length + self.call_count) & 255
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)


class LedStrip(object):

    def __init__(self):
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()
        self.color_strategy = FixedColorStrategy(Color(0, 0, 0))
        self.display_color()
        self.stop = False

    def set_color_strategy(self, color_strategy):
        self.color_strategy = color_strategy

    def display_color(self, animation_ms=0):
        """
        Set color across the strip one pixel at a time
        """
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, self.color_strategy.get_color(i))
            if animation_ms > 0:
                self.strip.show()
                time.sleep(animation_ms / 1000.0)

        self.strip.show()

    def theater_chase(self, animation_ms=50):
        """
        Movie theater light style chaser animation
        """
        while True:
            if self.stop:
                break

            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.color_strategy.get_color(i))
                self.strip.show()
                time.sleep(animation_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def pulse(self, animation_ms=100, step_size=2):
        """
        Pulse whatever is currently showing in the LED strip (brightness to zero brightness and back up)
        """
        brightness = 0
        going_up = True

        while True:
            if self.stop:
                break

            if brightness >= LED_BRIGHTNESS:
                going_up = False
            elif brightness <= 0:
                self.display_color()
                going_up = True

            self.set_brightness(brightness)
            brightness += step_size if going_up else -step_size
            time.sleep(animation_ms / 1000.0)

    def set_brightness(self, brightness=LED_BRIGHTNESS):
        """
        Set brightness for the whole led strip
        """
        brightness = LED_BRIGHTNESS if brightness > LED_BRIGHTNESS else brightness
        self.strip.setBrightness(brightness)
        self.strip.show()

    def off(self):
        self.set_color_strategy(FixedColorStrategy(Color(0, 0, 0)))
        self.display_color()


if __name__ == '__main__':
    strip = LedStrip()
    time.sleep(2)
    strip.set_color_strategy(RainbowColorStrategy())
    while True:
        strip.display_color()
        time.sleep(1 / 1000.0)

