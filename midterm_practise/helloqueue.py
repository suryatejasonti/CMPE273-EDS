from collections import deque

q = deque( maxlen=3 )
# deque([])



def get_index(element, queue):
    for i, ele in enumerate(queue):
        if ele == element:
            return i
    raise ValueError("{} is not in queue".format(element))

def append(element):
    try:
        index = get_index(element, q)
    except ValueError:
        q.append(element)


append( 10 )
append( 20 )
append( 30 )
# deque([ 10, 20, 30 ])

append( 40 )
append( 40 )
append( 40 )
append( 40 )
append( 10 )
print(q)