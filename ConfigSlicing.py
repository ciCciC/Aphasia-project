
class ConfigSlicing:

    """
    E.G
    # start = 0
    # end = 60000
    # MINUTE = 60000
    # interval = 500
    # silence_thresh = -40
    """

    start = 0
    end = 0
    MINUTE = 0
    interval = 0
    silence_thresh = 0

    def __init__(self, start, end, minute, interval, silenceThresh):
        """

        :param start: start of the audio chunk
        :param end: end of the audio chunk
        :param minute: time addition for the next minute
        :param interval: milliseconds interval, smaller = analyze more strictly E.G. 500ms
        :param silenceThresh: (dBFS) to address where to slice on the amplitude (Give negative number) E.G. -40 dBFS
        """
        self.start = start
        self.end = end
        self.minute = minute
        self.interval = interval
        self.silence_thresh = silenceThresh if silenceThresh < 0 else -silenceThresh