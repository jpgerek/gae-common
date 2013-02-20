# coding: utf-8
import time
import helpers

list = {
    'main.js': helpers.sha1(str(time.time())),
    'styles.css': helpers.sha1(str(time.time())),
    }
