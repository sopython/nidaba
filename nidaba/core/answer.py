
class Answer(object):
    """
    Stack Overflow Answer object which will hold information for use in Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: dict containing Answer information.
        :return: None
        """

        self.__data = data