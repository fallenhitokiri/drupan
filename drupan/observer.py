__author__ = "reed@reedjones.me"

from abc import ABC, abstractmethod
from typing import List, Any


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Any) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Any) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass


class ConcreteSubject(Subject):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """

    _state: str = None
    """
    For the sake of simplicity, the Subject's state, essential to all
    subscribers, is stored in this variable.
    """

    _observers: List[Any] = []
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    def attach(self, observer: Any) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Any) -> None:
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self, new_state: str = None) -> None:
        """
        Trigger an update in each subscriber.
        """

        if new_state:
            self._state = new_state

        if hasattr(self, 'context_name'):
            context_name = self.context_name
        else:
            context_name = self.__str__()
        for observer in self._observers:
            observer.update_context(context_name, self._state)


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass
