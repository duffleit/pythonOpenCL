import pyopencl as cl
import numpy as np


class OpenClRuntime:
    def __init__(self):
        self.context = cl.create_some_context()
        self.queue = cl.CommandQueue(self.context)

        self.array1 = np.eye(100, dtype=np.int32)
        self.array2 = np.eye(100, dtype=np.int32)

        self.load_program("multidimensionalAddition.cl")

    def load_program(self, filename):
        f = open(filename, 'r')
        fstr = "".join(f.readlines())
        self.program = cl.Program(self.context, fstr).build()

    def execute(self):
        array1Buf = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=self.array1)
        array2Buf = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=self.array1)

        output = np.zeros_like(self.array1, dtype=np.int32)
        outputBuf = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=output)

        self.program.add(self.queue, self.array1.shape, None, array1Buf, array2Buf, outputBuf)
        self.result = np.zeros_like(self.array1, dtype=np.int32)

        cl.enqueue_read_buffer(self.queue, outputBuf, self.result).wait();

    def print_out(self):
        for i in range(len(self.result)):
            output = "";
            for f in range(len(self.result)):
                output = output + " " + str(self.result[i][f]);

            print(output);

if __name__ == "__main__":
    runtime = OpenClRuntime();
    runtime.execute();
    runtime.print_out();
    print("End");
