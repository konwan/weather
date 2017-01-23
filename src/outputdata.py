# -*- coding: UTF-8 -*-
import os

class OutputData(object):
    def __init__(self):
        self.quote = True

    def outputData(self, datadir, filename, data):
        if not os.path.exists(datadir):
            os.makedirs(datadir)

        file = open(filename, 'w')

        for raw in data:
            if self.quote:
                formatdata = ["'{}'".format(i) for i in raw]
            else:
                formatdata = raw
            file.write("{}\n".format(",".join(formatdata)))
        file.close()

# if __name__ == "__main__":
#     a = OutputData()
#     print(a.quote)
