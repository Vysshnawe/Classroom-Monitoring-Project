def format_time(seconds):

    h = int(seconds//3600)
    m = int((seconds%3600)//60)
    s = int(seconds%60)

    return f"{h:02}:{m:02}:{s:02}"