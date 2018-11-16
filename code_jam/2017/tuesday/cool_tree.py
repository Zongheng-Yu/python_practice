#! /usr/bin/env python
import re


class TreeNode(object):
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.children = []
        self.task_packs = []

    def has_parent(self):
        return True if self.parent else False

    def depth(self):
        depth = 0
        node = self
        while node.has_parent():
            depth += 1
            node = node.parent

        return depth

    def get_result(self):
        result_pattern = '{%d, %s, %d}\r\n'
        count = 0
        for pack in self.task_packs:
            for each in pack.values():
                if not each:
                    count += 1
                    break

        if count == 0:
            return None
        return result_pattern % (self.depth(), self.key, count)

    def update_task_status(self, task, status):
        for pack in self.task_packs:
            if task in pack:
                pack[task] = status

    def add_task_pack(self, tasks):
        pack = {}
        for each in tasks:
            pack[each] = False

        self.task_packs.append(pack)

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

    def __str__(self):
        #return '%s:%s' % (self.key, str([each.key for each in self.children]))
        return '%s:%s' % (self.key, str(self.task_packs))


def add_node(src, target, tasks):
    print src
    if src not in g_nodes:
        g_nodes[src] = TreeNode(src)
    if target not in g_nodes:
        g_nodes[target] = TreeNode(target)

    g_nodes[target].parent = g_nodes[src]
    g_nodes[src].add_child(g_nodes[target])

    g_nodes[src].add_task_pack(tasks)
    if g_nodes[src] not in g_src_array:
        g_src_array.append(g_nodes[src])


def task_report(node, task, status):
    if node not in g_nodes:
        raise Exception('node not found: %s' % node)
    if status == 'Success':
        g_nodes[node].parent.update_task_status(task, True)


def main(input_file, output_file):
    node_pattren = re.compile('\{(\-?\d+), (\-?\d+), List\((.*)\)}')
    task_pattern = re.compile('\{(\-?\d+), (\-?\d+), ((Fail)|(Success))}')
    nodes_input = []
    task_reports = []
    with open(input_file) as fd_in:
        for each in fd_in:
            result = node_pattren.match(each)
            if result:
                #print each
                parent = result.groups()[0]
                child = result.groups()[1]
                tasks = result.groups()[2].replace(' ', '').split(',')
                nodes_input.append((parent, child, tasks))
            else:
                result = task_pattern.match(each)
                if result:
                    node = result.groups()[0]
                    task = result.groups()[1]
                    status = result.groups()[2]
                    task_reports.append((node, task, status))
                else:
                    print each
                    raise Exception(each)

    for each in nodes_input:
        add_node(each[0], each[1], each[2])
    for each in task_reports:
        task_report(each[0], each[1], each[2])

    lines = []
    for each in g_src_array:
        line = each.get_result()
        if line:
            lines.append(line)

    with open(output_file, 'wb') as fd_out:
        fd_out.writelines(lines)

if __name__ == '__main__':
    g_src_array = []
    g_nodes = {}
    main('StatOfDistTask.small.1496810642922.input', 'small.output')
    # main('StatOfDistTask.large.1496812435503.input', 'large.output')
