from multiprocessing import Process,Queue,cpu_count

def do_map(map_q,reduce_q,pid,map_fn,reduce_fn,perprocess_reduce_fn,args):
    output=[]
    while not map_q.empty():
        item = map_q.get()
        res=map_fn(item)
        output.append(res)

    if perprocess_reduce_fn:
        result = perprocess_reduce_fn(output)
        reduce_q.put(result)
    else:
        for item in output:
            reduce_q.put(item)
    return


def do_reduce(reduce_q):
    while not reduce_q.empty():
        item = reduce_q.get()
        res=map_fn(item)
        
    return
    

def task_mapreduce(map_fn,reduce_fn,iteration,pargs={},np=None,perprocess_reduce_fn=None):
    tasks = []
    map_q = Queue()
    reduce_q = Queue()
    for item in iteration:
        map_q.put(item)
    n = np if np is not None else cpu_count()
    for i in range(n):
        pro = Process(target=do_map, args=(map_q,reduce_q,i,map_fn,reduce_fn,perprocess_reduce_fn,pargs))
        pro.start()
        tasks.append(pro)

    print('waiting for task complete')
    for task in tasks:
        task.join()

    if reduce_fn:
        do_reduce(reduce_q)
    print('tasks end')
    print('mp_extract_market_feature end-{}'.format(datetime.datetime.now()))

