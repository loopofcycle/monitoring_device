from abc import ABC
import os, pprint

class Observable(ABC):
    _observers = {}

    def __init__(self, name):
        print('initialized - ', self)
        self.name = name
        self.value = 'test'
        self._observers = {}

    def __setattr__(self, name, value):
        print('__setattr__', self, name, value)
        super().__setattr__(name, value)
        self.notify(name, value)
    
    def notify(self, subject, value):
        print('notify', self, subject, value)
        print('observers.keys()', self._observers.keys())
        if subject in self._observers.keys():
            for observer in self._observers[subject]:
                observer.receive_notification(value)

    def add_observer(self, observer, subject = 'value'):
        if subject in self._observers.keys():
            self._observers[subject].append(observer)
            print('to:',self,'on to subject:',subject,'added observer:', observer)
        if subject not in self._observers.keys():
            self._observers[subject] = [observer]
            print('to:',self,'on to subject:',subject,'added observer:', observer)
        pprint.pprint(self._observers)

class Observer():b
    def __init__(self):
        print('initialized - ', self)

    def receive_notification(self, notification):
        print(self, 'received value', notification)

if __name__ == '__main__':
    observer1 = Observer()
    observer2 = Observer()
    sensor = Observable('tempeture')
    sensor.add_observer(observer1)
    sensor.add_observer(observer2)
    sensor.value = '42'
