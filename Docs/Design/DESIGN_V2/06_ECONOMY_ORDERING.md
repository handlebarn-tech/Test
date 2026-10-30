# 06 — ECONOMY & ORDERING SIMULATION

## 1. Goal
Create non-obvious choices about assortment, depth, cash, storage, lead time and demand without building accounting software.

## 2. Economic state
Authoritative:
- `CashAvailable`
- `CommittedPurchaseCash`
- `OperatingReserve`
- `InventoryAcquisitionValue`
- `Revenue`
- `DiscountCost`
- `COGS`
- `WasteCost`
- `LaborBudgetUnits`
- `StorageCapacityByZone`
- `SupplierAvailability`
- `PurchaseOrders`

## 3. What is intentionally abstracted
Do not simulate by default:
- full general ledger;
- payroll tax;
- depreciation;
- balance sheet;
- vendor invoice reconciliation beyond gameplay exceptions;
- detailed rent/utilities.

## 4. Shift contribution metric

`NetSales = GrossSales - Discounts`

`COGS = sum(soldQty * acquisitionCost)`

`Contribution = NetSales - COGS - WasteCost - VariableLaborCost`

This is a game-management metric, not GAAP profit.

## 5. Purchasing budget

`PurchasingHeadroom = CashAvailable - CommittedPurchaseCash - OperatingReserve`

Default OperatingReserve target: 25% of forecast two-shift operating spend, configurable 20–35%.

Orders cannot commit negative headroom unless an authored scenario explicitly enables emergency financing; default game has no debt mechanic.

## 6. Demand model
Demand is generated at the **need/category** level first, then product preference is applied.

Inputs:
- historical demand by need/category;
- repeat-customer pool;
- deal modifiers;
- day/shift profile;
- product/category availability;
- scenario events;
- seasonal/campaign modifier only if explicitly authored.

Forecast is a distribution, not a future customer list.

Manager sees:
- expected demand;
- low/high band;
- recent trend;
- stock cover;
- forecast confidence.

## 7. Safety stock
**OUTSIDE-RESEARCH-INFORMED NEW PROPOSAL:** buffer responds to demand and lead-time variability.

For a SKU/batch family with approximately independent demand and lead time:

`SafetyStock = z * sqrt(L_mean * sigma_demand^2 + demand_mean^2 * sigma_lead^2)`

All units expressed per shift.

This is an internal planning quantity. The UI may summarize it as risk bands.

### Service classes
Initial game tuning:
- Coverage-critical/core: target 95%, `z≈1.65`
- Normal/core: target 92%, `z≈1.41`
- Opportunistic/niche: target 85%, `z≈1.04`

Class is based on service coverage/value, not margin alone.

## 8. Reorder point

`ReorderPoint = ExpectedDemandDuringLeadTime + SafetyStock`

`OrderUpTo = ReorderPoint + ReviewPeriodDemand`

Routine review period initial target: every 2 shifts.

## 9. Supplier model

```yaml
SupplierOffer:
  supplier_id
  item_or_batch_id
  acquisition_cost
  minimum_order_qty
  lead_time_mean_shifts
  lead_time_sd
  fill_rate
  delivery_windows
  available_qty
  deal_terms
```

Normal initial ranges:
- lead time 1–3 shifts;
- fill rate 88–100%;
- emergency replenishment premium 8–20% where available;
- emergency lead time 1 shift minimum, never instant.

## 10. Assortment: breadth vs depth
Every order competes across:
- **breadth**: number of distinct customer need/category paths covered;
- **depth**: units/grams behind likely demand;
- **cash**: purchase capacity left;
- **space**: physical storage left;
- **lead risk**: likelihood replenishment arrives late;
- **aging/expiry risk** where applicable.

The order UI must show all six.

## 11. Recommendation Coverage Score
To keep ordering connected to the floor, calculate a descriptive coverage metric:

`CoverageScore = weighted share of forecast customer need profiles for which at least one currently/prospectively stocked eligible path exists`

This uses customer need categories + canonical TFS eligibility/output as an oracle when practical. It does **not** create a new recommendation ranking.

CoverageScore is advisory. A manager can intentionally choose lower coverage for depth/cash reasons.

## 12. Inventory risk states
Per item/batch/location:
- `HEALTHY`
- `LOW`
- `CRITICAL`
- `EMPTY_WITH_BACKSTOCK`
- `SOLD_OUT`

For planning, also expose:
- `OVERSTOCK_RISK`
- `EXPIRY_RISK` if the product has an actual configured expiry/sell-by horizon.

Do not invent chemistry degradation from age. Aging affects economic/expiry risk only unless canonical product data says otherwise.

## 13. Expiry/aging
Use real configured expiry where product categories have one.

`ProjectedUnitsAtExpiry = OnHand - ForecastDemandUntilExpiry`

Risk bands:
- Safe: projected <=0 before expiry or ample sell-through.
- Watch: projected leftover <=25% of on-hand.
- At Risk: 25–60% projected leftover.
- Critical: >60% projected leftover or expiry inside one review period.

Deli flower should not receive fabricated potency loss mechanics.

## 14. Deals
Deal object:

```yaml
Deal:
  eligible_items
  discount_rule
  start_shift
  end_shift
  expected_demand_lift_band
  inventory_requirement
  cooldown_or_frequency_rule
```

Deal consequences:
- lower realized margin;
- demand displacement;
- queue/retrieval load;
- stockout risk;
- potentially better sell-through of at-risk inventory.

Deals are not a free traffic buff.

## 15. Labor abstraction
Manager chooses staffing capacity and capability mix, not payroll line items.

`LaborCost = scheduledStaffHours * roleCostIndex`

RoleCostIndex can be normalized rather than denominated in real dollars.

## 16. Storage
Track independent capacity:
- deli jar/FOH;
- packaged fast-access FOH;
- BOH ambient;
- cold storage;
- cooler/perishable;
- receiving staging.

A purchase order that cannot physically fit must either:
- be reduced;
- arrive after planned sell-through;
- require planned space reallocation.

No magical warehouse overflow.

## 17. Ordering UI
For each proposed line show:
- on hand;
- on order;
- forecast demand band until next possible replenishment;
- target safety stock;
- projected cover;
- acquisition cost;
- space use;
- supplier lead/fill risk;
- coverage contribution;
- expiry risk.

Order summary shows:
- cash after commitment;
- storage after expected receipt;
- expected coverage;
- top 5 residual stockout risks;
- top 5 overstock risks.

## 18. Planning loop
`review demand -> inspect coverage/risk -> choose breadth/depth -> submit order -> supplier uncertainty -> receive -> allocate FOH/BOH -> serve shifts -> observe lost sales/stockouts -> revise`

## 19. Stylized policy stress test
A deliberately simplified 18-SKU/6-need-cluster simulation was used to check whether constraints create tradeoffs. It is not tuning authority.

Over 45 Monte Carlo seeds x 50 shifts:

| Policy | fill rate | mean contribution | unmet demand | waste | holding burden | ending inventory value |
|---|---:|---:|---:|---:|---:|---:|
| Balanced | 81.0% | 2736.8 | 79.2 | 4.0 | 207.4 | 140.2 |
| Breadth | 79.2% | 2460.9 | 87.7 | 3.9 | 159.1 | 105.6 |
| Depth | 74.2% | 1989.8 | 106.4 | 1.6 | 164.2 | 107.7 |
| Margin-only | 62.2% | 2705.0 | 158.9 | 0.3 | 130.4 | 69.6 |
| Order-everything | 97.7% | 2581.4 | 9.8 | 71.0 | 549.4 | 371.9 |

Interpretation: maximizing fill through “order everything” carries materially larger holding/waste; margin-only can look financially competitive while providing poor service coverage. Therefore the game needs both economic and service/coverage consequences rather than one universal objective.

## 20. Dominant-strategy controls
- margin-only: coverage/retention/lost-sale consequences;
- cheapest-only: weaker demand coverage and potentially lower contribution;
- order-everything: cash, storage, waste/expiry and receiving load;
- zero safety stock: stockouts + emergency premium;
- extreme safety stock: tied cash/space;
- deal spam: margin + stock + operational cost;
- emergency-order spam: premium, limited supplier availability, lead delay.

## 21. Manager report attribution
For every lost sale, attempt to classify:
- no viable product ever stocked;
- stocked but sold out;
- product in BOH but unavailable on floor at decision time;
- price/budget mismatch;
- wait abandonment;
- customer voluntary decline.

This makes ordering decisions learnable.

## 22. Acceptance criteria
- ordering changes later floor inventory through InventoryService only;
- no policy dominates across all seeds/scenarios;
- a high-margin narrow order can lose on coverage;
- order-everything can lose on cash/space/waste;
- forecast never exposes exact future customers;
- safety stock responds to uncertainty parameters;
- expiry risk never changes TFS chemistry.
