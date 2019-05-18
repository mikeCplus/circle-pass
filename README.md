## Circle Pass

An attempt at a simple, novel, secure password scheme.

**Code written by Mike Cichonski. 
Documentation and analysis by Mike Cichonski, Shane Slatter, Grayson Lafreniere, and Shrey Shree.**

### Install and Run

##### Linux and Mac

1. Download this project by opening a Terminal window, navigating to a desired download directory, and cloning this project:

	```bash
	>> cd /directory/to/download/
	>> git clone https://github.com/mikeCplus/circle-pass
	```

2. Change directory to the cloned circle-pass folder and run with Python 2 or 3:

	```bash
	>> cd circle-pass
	>> python circlePass.py
	```

##### Windows

1. Download this project from [here](https://github.com/mikeCplus/circle-pass) and clicking the `[ Clone or download ]` button.

2. Download Python from [here](https://www.python.org/downloads/).

3. Double-click the `circlePass.py` file to run with Python.

### Description

This is a small app which began as a school group project. It is an attempt to create a novel, intuitive, and secure password scheme at three levels of security:  

1. Phone (4x4 grid)
2. Facebook (7x7 grid)
3. Bank (10x10 grid)  

With this password scheme we attempted to accommodate for users’ differing learning styles. Some might be better visual learners while others might be better with numbers so we created a password scheme that allows for different memorization techniques. It makes use of both visual and text-based cues to help with password memorization, which engages multiple areas of the brain, further aiding the memorization process. 

The biggest drawback to this scheme is a possibility of shoulder surfing, although it appears to be quite difficult to remember the locations of the circles after just one viewing which is why the user gets three rounds of training for each password. Although this does pose some risk to security, in almost all cases this drawback would be greatly outweighed by the usability aspects of the scheme.

The password scheme has a very simple interface with very constrained interaction (the circles appear to be the only thing that can be ‘manipulated’ in any way), which makes it obvious very quickly how the scheme works. It is also similar to other grid-based schemes and even visually comparable to the recently standardized 9-dot phone patterns which makes learnability almost instantaneous. The interaction also works smoothly with messages guiding the user through every step. Due to the visual on-screen nature of the scheme, it is ideal for touch screen based machines such as phones and tablets, and it appeared to be faster for users who used the touch screen versus those who clicked and dragged the mouse. 

Although the password space of the Phone password (4 values in a 4x4 grid space) does not reach 2^28, which would be a sufficient level of security for a phone, the grid size can easily be adjusted to greatly expand the space and meet that requirement. A 4-value password would require a 14x14 grid to meet the 2^28 requirement, which is only a few squares larger than the Bank password space (all calculations below). The idea is that expanding grid size only slightly increases the difficulty of remembering the password (at least numerically) as long as the number of circle values to remember remains constant. I settled for a 4-number password because this can still easily be stored in working memory while allowing for a theoretically large enough space. A 5-number password might also be a reasonable option, but any more than that would make it exceedingly difficult to remember because the values are numbers, not just digits (0-9). Any less than 4 would make the password space too small, but still might be reasonable for a phone password. The values may also be duplicates (the circles can overlap onto the same square) which increases the password space as well. Below is a table of calculations for different grid sizes of the password space given 4 circles. Given that duplicates are allowed, the calculations are very simple.

| Grid Size | Password Space | Total Possibilities | Goal (2^28) |
|-----------|----------------|---------------------|-------------|
|   4x4     |      4^4       |         256         | 268,435,456 |
|   7x7     |      4^7       |       16,384        | 268,435,456 |
|  10x10    |      4^10      |      1,048,576      | 268,435,456 |
|  12x12    |      4^12      |     16,777,216      | 268,435,456 |
|  14x14    |      4^14      |    268,435,456      | 268,435,456 |

