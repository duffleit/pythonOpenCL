__kernel void add(__global int* input1, __global int* input2, __global int* output){
    int id0 = get_global_id(0) * get_global_size(0);
    int id1 = get_global_id(1);

    int id = id0 + id1;
    output[id] = input1[id] + input2[id];
}
