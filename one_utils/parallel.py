from multiprocessing import Process,Queue,cpu_count,Manager

def do_map(map_q,reduce_q,pid,map_fn,map_wrapper,reduce_fn,perprocess_obj_init,perprocess_reduce_fn,args):
    output=[]
    perprocess_obj=None
    if perprocess_obj_init:
        perprocess_obj=perprocess_obj_init()
    while not map_q.empty():
        item = map_q.get()
        try:
            if map_wrapper:
                res=map_wrapper(item,perprocess_obj=perprocess_obj)
            else:
                res=map_fn(item)
        except Exception as e:
            print('Exception {} in mapping item {}'.format(e,item))
            res = None
        output.append(res)

    if perprocess_reduce_fn:
        result = perprocess_reduce_fn(output)
        reduce_q.put(result)
    else:
        for item in output:
            reduce_q.put(item)
    return


def do_reduce(reduce_q,reduce_fn,reduce_initializer):
    res=reduce_initializer
    while not reduce_q.empty():
        item = reduce_q.get()
        res=reduce_fn(res,item)
        
    return res
    

def mapreduce_mp(iteration,map_fn=None,map_wrapper=None,reduce_fn=None,pargs={},np=None,perprocess_obj_init=None,perprocess_reduce_fn=None,reduce_initializer=None):
    tasks = []
    map_q = Manager().Queue()
    reduce_q = Manager().Queue()
    print('start distribute data')
    for item in iteration:
        map_q.put(item)
    n = np if np is not None else cpu_count()
    print('start process')
    for i in range(n):
        pro = Process(target=do_map, args=(map_q,reduce_q,i,map_fn,map_wrapper,reduce_fn,perprocess_obj_init,perprocess_reduce_fn,pargs))
        pro.start()
        tasks.append(pro)

    print('waiting for task complete')
    for task in tasks:
        task.join()
    print('after for task complete')

    output=[]

    if reduce_fn:
        return do_reduce(reduce_q,reduce_fn,reduce_initializer)
    else:
        while not reduce_q.empty():
            item = reduce_q.get()
            output.append(item)
        return output
        

