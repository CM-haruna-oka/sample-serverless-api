import dataclasses


@dataclasses.dataclass(frozen=True)
class Amount:
    amount: int
    currency: str

    def __eq__(self, other):
        return (self.amount == other.amount) and \
               (self.currency == other.currency) and \
            isinstance(other, Amount)


amount1 = Amount(220, 'jpy')
amount2 = Amount(1100, 'jpy')
amount3 = Amount(1100, 'jpy')
print(amount1 == amount2)     # True
print(amount2 == amount3)     # False
