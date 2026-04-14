from market.sim.agents.strategy_interface import Strategy, Observation, OrderRequest
from market.sim.exchange.order import Side, OrderType
from typing import Dict, List
from collections import defaultdict, deque


class FinalStrategy(Strategy):

    def __init__(self):
        super().__init__()

        self.window = 10
        self.max_position = 500
        self.news_qty_initial = 500

        self.history = defaultdict(lambda: deque(maxlen=self.window))

        self.in_trade = defaultdict(bool)
        self.direction = defaultdict(int)
        self.entry_price = defaultdict(float)
        self.hold_ticks = defaultdict(int)

    def act(self, observations: Dict[str, Observation]) -> List[OrderRequest]:
        orders = []

        for commodity, obs in observations.items():

            mid = obs.midprice
            if mid is None:
                continue

            self.history[commodity].append(mid)
            if len(self.history[commodity]) < self.window:
                continue

            pos = int(obs.position)
            news = obs.news.get(commodity, 0)

            # =========================
            # MANAGE TRADE
            # =========================
            if self.in_trade[commodity]:

                self.hold_ticks[commodity] += 1
                d = self.direction[commodity]

                # 1. FORCE EXIT ON OPPOSITE NEWS
                if (d > 0 and news < 0) or (d < 0 and news > 0):
                    if pos != 0:
                        side = Side.ASK if d > 0 else Side.BID
                        orders.append(OrderRequest(side, OrderType.MARKET, abs(pos), commodity))
                    self._reset(commodity)
                    continue

                # 2. SOFT STOP LOSS (PREVENT BLOWUPS)
                if d > 0:
                    loss = (self.entry_price[commodity] - mid) / self.entry_price[commodity]
                else:
                    loss = (mid - self.entry_price[commodity]) / self.entry_price[commodity]

                if loss > 0.015:  # 1.5% loss cutoff
                    if pos != 0:
                        side = Side.ASK if d > 0 else Side.BID
                        orders.append(OrderRequest(side, OrderType.MARKET, abs(pos), commodity))
                    self._reset(commodity)
                    continue

                # 3. OPTIONAL SAFETY EXIT (VERY LONG HOLD)
                if self.hold_ticks[commodity] > 300:
                    if pos != 0:
                        side = Side.ASK if d > 0 else Side.BID
                        orders.append(OrderRequest(side, OrderType.MARKET, abs(pos), commodity))
                    self._reset(commodity)
                    continue

                continue

            # =========================
            # ENTRY
            # =========================
            if news > 0 and pos == 0:
                orders.append(OrderRequest(
                    side=Side.BID,
                    order_type=OrderType.MARKET,
                    quantity=self.news_qty_initial,
                    commodity=commodity
                ))

                self.in_trade[commodity] = True
                self.direction[commodity] = 1
                self.entry_price[commodity] = mid
                self.hold_ticks[commodity] = 0
                continue

            if news < 0 and pos == 0:
                orders.append(OrderRequest(
                    side=Side.ASK,
                    order_type=OrderType.MARKET,
                    quantity=self.news_qty_initial,
                    commodity=commodity
                ))

                self.in_trade[commodity] = True
                self.direction[commodity] = -1
                self.entry_price[commodity] = mid
                self.hold_ticks[commodity] = 0
                continue

        return orders

    def _reset(self, c):
        self.in_trade[c] = False
        self.direction[c] = 0
        self.hold_ticks[c] = 0