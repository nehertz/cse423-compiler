class Person:
    def __init__(self):
        self.name = 'yash'

    def get_name(self, name):
        print('name is ' + name)


if __name__ == '__main__':
    p = Person()
    getattr(p, 'get_name')('ripa')
    # p.get_name('ripa')
