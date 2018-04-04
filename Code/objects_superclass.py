#First Tier (Super class)
class Task:
    task_count = 0 #to access taskcount just, Task.taskcount
    tabu_freq = 0
    def __init__(self, resource_reqd, tabu_tenure):
        self.resource_reqd = resource_reqd
        self.tabu_tenure = tabu_tenure
        Task.task_count += 1
    def get_resource_reqd(self):
        return self.resource_reqd
    def get_tabu_tenure(self):
        return self.tabu_tenure
    def get_tabu_freq(self):
        return self.tabu_freq
    def tabu_tenure_expiry(self):
        self.tabu_tenure += -1
class Resource:
    resource_count = 0
    def __init__(self):
        Resource.resource_count += 1

#Testing
# test_task = Task(['satellite'],1)
# print(test_task)
# print(test_task.get_resource_reqd())
# print(test_task.get_tabu_tenure())
# print(test_task.task_count)
# print("-------------------------------------------------------------------------")
# test_task2 = Task(['satellite','groundstation'],1)
# print(test_task2)
# print(test_task2.get_resource_reqd())
# print(test_task2.get_tabu_tenure())
# print(test_task2.task_count)
# print("-------------------------------------------------------------------------")
# test_resource = Resource()
# print(test_resource)
# print(test_resource.resource_count)
