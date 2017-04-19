

class FindLongestLineInFile(object):
    @staticmethod
    def traditional_way(file_name):
        longest = 0
        with open(file_name, 'rb') as fd:
            for line in fd:
                length = len(line.strip())
                if length > longest:
                    longest = length

        return longest

    @staticmethod
    def list_comps(file_name):
        with open(file_name, 'rb') as fd:
            return max([len(line.strip()) for line in fd])

    @staticmethod
    def generator(file_name):
        with open(file_name, 'rb') as fd:
            return max(len(line.strip()) for line in fd)

if __name__ == '__main__':
    print FindLongestLineInFile.traditional_way("example.log")
    print FindLongestLineInFile.list_comps("example.log")
    print FindLongestLineInFile.generator("example.log")
