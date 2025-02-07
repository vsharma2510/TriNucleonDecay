



def Main(  
    Filepath = None,
    WriteText = None,
    ):

    FileHandle = open(Filepath, 'w')
    FileHandle.write(WriteText)
    FileHandle.close()

    return True



