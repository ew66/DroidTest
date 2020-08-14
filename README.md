# Introduction

An auto testing tool to script your test procedure on android devices.

# Preparation

You have to describe 
- the touch position of your each **Touch Action** in the `touchActions.tab`  
    format is `[Action name]: pos_x pos_y`

- the start and end position of your each **Swipe Action** in the `swipeActions.tab`  
    format is `[Action name]: pos_start_x pos_start_y pos_end_x pos_end_y`

# Usage
```
usage: DroidTest.py [-h] [-s SERIAL] [--touch-table TOUCH_ACTION_TABLE]
                         [--swipe-table SWIPE_ACTION_TABLE]
                         [--interval ACTION_INTERVAL] [-t REPEAT_COUNT]
                         [-p PROCEDURE]
                         [ACTION [ACTION ...]]

This is broken from Baliji, but crashed by Muhammand

positional arguments:
  ACTION                actions to be performed in a single flow. Format:
                        action_name,delay_ms

optional arguments:
  -h, --help            show this help message and exit
  -s SERIAL, --serial SERIAL
                        serial# of the device, use this argument if you have
                        2+ devices
  --touch-table TOUCH_ACTION_TABLE
                        the name of touch action table. default:
                        touchActions.tab
  --swipe-table SWIPE_ACTION_TABLE
                        the name of swipe action table. default:
                        swipeActions.tab
  --interval ACTION_INTERVAL
                        the internal between two actions. default: 2s
  -t REPEAT_COUNT, --repeat REPEAT_COUNT
                        the number of times to repeat assigned actions.
                        default: 1
  -p PROCEDURE          the name of repeat procedure. ex: example.procedure
```