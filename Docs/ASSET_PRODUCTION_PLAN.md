# DISPENSARY GAME — ASSET PRODUCTION PLAN
## Free Asset Research, Reality Reconstruction, Custom Modeling & Procedural Art Pipeline

**Version:** 2.0  
**Date:** 2026-10-29  
**Parent:** `MASTER_PLAN.md`  
**Load policy:** Art/technical-art/reference workers only. The Studio Hub should not keep this entire file in routine context.

---

# A. Purpose and context policy

This document owns:

- physical-store visual analysis;
- free asset sourcing;
- author/license/source references;
- room-by-room Bill of Assets;
- custom-model backlog;
- Blender generators;
- procedural product/stock systems;
- materials;
- lighting asset strategy;
- character/audio source research where art production requires it;
- asset QA;
- provenance.

It intentionally does **not** own:
- project roadmap;
- Unity gameplay migration;
- agent-studio governance.

Workers should receive only the relevant section plus task-specific references.

---

# B. Hard constraints

- $0 third-party asset budget.
- $0 required software budget.
- Free does not justify low quality.
- Store-identifying geometry is custom-built.
- Generic complex objects may use strong free assets.
- Repeated objects are proceduralized.
- Every third-party asset has provenance/license metadata.
- No ripped game assets.
- No unclear provenance.
- Realism outranks generic cannabis aesthetic.

---

# C. Canonical art goal

> Reconstruct the supplied dispensary closely enough that its identity comes from architecture, fixtures, density, materials, operational clutter and lighting—not from random weed-themed decoration.

The sections below contain the detailed research and production specification.

---

# 0. Final decision

The project does **not** need paid assets to reach a high visual standard.

The correct approach is a hybrid:

> **CUSTOM MODEL what identifies this exact store.  
> DOWNLOAD FREE what is generic but expensive to recreate.  
> PROCEDURALLY VARY what repeats hundreds of times.**

The first research pass over-relied on paid Unity/Fab assets. This version removes that assumption and rebuilds the sourcing strategy around:

1. **Poly Haven — CC0** high-end scans, PBR materials, utility props, furniture, lights, plants and industrial assets.
2. **Unity Technologies Japan — free Unity Warehouse + UnityJapanOffice** as high-quality HDRP donor libraries.
3. **Sketchfab — carefully selected CC BY / free-standard models** for cannabis-specific objects, security hardware, POS devices and niche props.
4. **Fab — free individual models** only where the asset is genuinely useful and quality is acceptable.
5. **MakeHuman / free character sources + free mocap** for NPCs.
6. **Sonniss / Pixabay / other free audio libraries** for professional ambience and interaction sounds.
7. **Blender** for everything that is store-specific or where free alternatives fail the visual match.

The major implication is important: **do not lower the art standard just to avoid spending money.**  
When a free asset is visibly wrong, model the object yourself from the supplied references.

---

# 1. Reality reconstruction target

## 1.1 Building geometry established by the supplied floor plan

The supplied plan gives the following room schedule:

| Area | Approximate area |
|---|---:|
| Retail / sales floor | 1,373.31 sq ft |
| HUB | 818.53 sq ft |
| HUB 2 | 541.34 sq ft |
| FOH floor-restock | 163 or 180 sq ft |
| BOH backstock | 163 or 180 sq ft |
| Break room | 151.56 sq ft |
| Office | 131.82 sq ft |
| Restroom | 53.16 sq ft |
| Hall | 35.16 sq ft |
| Janitor closet | 19.19 sq ft |
| **Net room area** | **3,467.77 sq ft** |
| **Building gross** | **~3,590 sq ft** |

The plan also gives a highly useful approximate building footprint and room arrangement. The retail area is roughly **47 ft wide by 29 ft deep**, followed by the small-room band and then the two large rear HUB spaces.

### Sales-floor anchors that must be reproduced

- West customer entrance
- ATM near entry
- Queue / stanchion field
- Register run, up to 12 stations
- Main deli counter
- Deli flower jar walls
- Living / green wall
- Menu screen
- Merchandise wall
- Glass display case
- Two white columns
- East emergency exit
- Hand-wash sink
- Globe/pendant lighting
- Arch openings toward the back-room band

### Back-of-house anchors

- Hall with black doors and notices
- Office with L-desk, computer equipment, paper workflow, safes and IT rack
- Break room with wood cabinets, black/dark counter, sink, microwave, coffee equipment and bench/seating
- FOH restock room with chrome wire racks, bins, refrigerator and totes
- BOH backstock with cased product, kraft bags and wire racks
- HUB with desks/computers, deliveries and general storage
- HUB2 as secondary storage connected from HUB
- Exterior employee-only delivery access

---

# 2. CCTV composite: visual analysis by camera tile

The supplied camera-wall composite is a **5 × 5 grid**. It is far more valuable than a polished promotional photograph because it shows the building in its actual working state.

The exact camera-to-room mapping is only partially documented, so the labels below distinguish **observed content** from **room inference**.

## Row 1 — exterior

### R1C1
Observed:
- Large asphalt field
- Painted parking lines
- Concrete curb/sidewalk edge
- Parked crossover/SUV
- Security-camera night exposure
- Large low-detail open space rather than decorative landscaping

Asset implications:
- Real asphalt PBR
- Parking-stripe decals
- Concrete curb
- Generic mid-detail parked cars
- Strong exterior security light / sodium-or-neutral night exposure preset

### R1C2
Observed:
- Rear/side service parking
- Light-colored commercial exterior wall
- Dark privacy/gate zone
- Multiple parked vehicles
- Yellow pavement/curb marking
- Flat-roof commercial context

Asset implications:
- Custom shell
- Privacy fencing/gate
- Utility wall details
- HVAC/electrical/conduit clutter
- Parking-lot vehicles

### R1C3
Observed:
- Long building wall
- Dark green gate or fence section
- Yellow-painted curb / edge
- Several parked cars
- Bright overhead exterior lighting

Asset implications:
- Green privacy barrier
- Photometric wall packs / exterior floods
- Weathered asphalt
- Custom building material

### R1C4
Observed:
- Parking/drive aisle
- Orange traffic cone
- Hedge/shrub mass
- Crosshatched yellow pavement markings
- Vehicle headlights creating harsh camera bloom

Asset implications:
- Traffic cone
- Hedge
- parking/accessible/crosshatch decal set
- headlight emissive/light behavior

### R1C5
Observed:
- Front/side parking
- Multiple vehicles
- Sidewalk / pedestrian approach
- Storefront/building edge
- Security lighting

Asset implications:
- Vehicle variety
- curb cuts
- sidewalk panels
- entrance-area details

## Row 2 — main retail floor

Across all five feeds:
- Light marble/stone-pattern floor
- Black/dark counters
- Green brand accents
- Wood retail finishes
- Queue stanchions with black belts
- POS monitors
- Product shelving / jar wall
- Bright wall/menu screens
- Customers and staff
- High product density
- Decorative globe/round fixtures
- Repeated register hardware
- Glass display elements

This row establishes the most important realism rule:

> **The room is dense, operational, and imperfectly occupied. It is not a sparse luxury showroom.**

## Row 3

### R3C1
Observed:
- Exterior sidewalk
- Hedge against building
- Narrow pedestrian strip
- Hard security-light contrast

### R3C2
Observed:
- Sales-floor edge / rear retail viewpoint
- POS/display hardware
- Product cases
- Retail shelving
- Dense counter clutter

### R3C3 — office
Observed:
- L-shaped workstation
- Computer monitor(s)
- Paper / cup / personal-object clutter
- Whiteboard or wall information surface
- Cabinetry / storage
- Chair
- Work area that looks actively used

### R3C4 — hall
Observed:
- Black commercial doors
- Employee/restricted signage
- Bulletin/corkboard and printed notices
- Black-and-white patterned tile
- Narrow utilitarian corridor
- Door hardware and trim

### R3C5 — break room
Observed:
- Wood cabinet run
- Counter
- sink
- small appliances
- wall posters/notices
- seating/bench/chairs
- black door
- miscellaneous employee belongings

## Row 4

### R4C1 — likely FOH/restock
Observed:
- Chrome wire shelving
- packaged inventory
- yellow-lid tote/bin
- small floor area
- black doors
- strong utility lighting

### R4C2 — backstock
Observed:
- Very narrow storage aisle
- cardboard cases
- wire shelves
- stacked product
- high storage density

### R4C3
Observed:
- Large chrome/wire storage structures
- orange shelving
- cased product
- utilitarian concrete/service-floor appearance

### R4C4
Observed:
- Wire-rack inventory
- blue plastic totes
- boxes
- open central aisle

### R4C5
Observed:
- Same office view family as R3C3
- reinforces workstation/counter/paper/appliance clutter

## Row 5 — rear storage / HUB / BOH family

Across the five feeds:
- Large quantities of blue totes
- yellow lids
- cardboard cases
- metal shelving
- wire cages/rack structures
- carts
- narrow working aisles
- irregular stack heights
- dense inventory
- utilitarian lighting
- very little decorative finish

This is critical: **the rear half of the game should look like a real small distribution/retail back room, not like empty gray rooms with a few boxes.**

---

# 3. Public reference cross-check

Use the public pages below only as **reference material** unless the image/license explicitly allows direct reuse.

- The Flower Shop Phoenix menu / store reference:  
  https://theflowershopusa.com/menu/phoenix/flower
- Leafly Phoenix listing / photos / current categories:  
  https://www.leafly.com/dispensary-info/the-flower-shop-phoenix

The current store/menu references reinforce:
- very large flower assortment
- bulk/deli flower as a real product category
- pre-rolls
- concentrates
- vapes
- edibles
- topicals
- accessories

That means a believable sales floor needs **multiple package form factors**, not just jars of flower.

---

# 4. Engine choice: Unity 6.3 LTS + HDRP

> *(superseded by DEC-003: the project uses Unity 6000.6.7f1 + HDRP 17.6.0)*

For this specific project, moving away from a browser-first Three.js scene is recommended.

Unity opens:
- HDRP physical lighting
- physically based decals
- reflection probes
- Adaptive Probe Volumes / baked GI workflows
- mature animation retargeting
- NavMesh / AI Navigation
- occlusion culling
- LOD Groups
- GPU instancing
- prefab variants
- RenderTextures for CCTV feeds
- easier Blender/FBX/glTF asset workflows
- much larger free asset ecosystem

### Recommended rendering baseline

- Unity 6.3 LTS *(superseded by DEC-003: the project uses Unity 6000.6.7f1 + HDRP 17.6.0)*
- HDRP
- Linear color space
- physical light units
- real-world metric scale
- baked/static GI where practical
- probes for dynamic NPCs
- decals for wear and labels
- physically correct glass, not generic transparent Standard materials
- GPU instancing for jars, packages, boxes and repeated shelving contents
- high-resolution hero materials only where the player gets close

---

# 5. Free-asset license strategy

## Preferred order

1. **CC0 / public domain** — best.
2. **CC BY** — free; maintain an attribution ledger.
3. **Unity Asset Store free assets** — use under the Unity Asset Store EULA.
4. **Fab / Sketchfab Free Standard** — inspect current terms before download.
5. **Personal/non-commercial-only free assets** — acceptable for this private project, but keep them isolated and documented in case the project is ever shared.

### Important

This project is currently private and non-commercial. If that changes, **re-audit every third-party asset and every real-world brand/logo before distribution.**

### Provenance rule

Do not use models that were obviously extracted from GTA, another game, or an unclear copyrighted source even if someone has uploaded them for free. There are enough legitimate free alternatives.

---

# 6. Core free libraries

## Poly Haven — primary visual-quality source
**License:** CC0  
https://polyhaven.com/  
https://polyhaven.com/license

Best use:
- 8K PBR materials
- industrial props
- furniture
- lights
- CCTV
- HVAC / utilities
- plants
- exterior props
- HDRIs for Blender reference renders

## Unity Warehouse — Unity Technologies Japan
**Cost:** Free  
**Pipeline:** HDRP  
https://assetstore.unity.com/packages/3d/environments/industrial/unity-warehouse-276394

Best use:
- shelving
- cargo
- warehouse dressing
- transport equipment
- BOH/HUB donor assets
- photoreal reference for HDRP material setup

## UnityJapanOffice — Unity Technologies Japan
**Cost:** Free  
**Pipeline:** HDRP project  
https://assetstore.unity.com/packages/3d/environments/unityjapanoffice-152800

Best use:
- office furniture
- electronics
- realistic interior props
- material/shader reference
- break-room / workstation donors

## Sketchfab
https://sketchfab.com/

Use selectively. Search for:
- downloadable
- CC BY / CC0
- game-ready where possible
- clean source provenance

## Quaternius
https://quaternius.com/
License information: https://quaternius.com/license.html

Excellent zero-cost library, but much of it is stylized/low-poly. Use mainly for background or hidden utility objects unless the asset visually matches.

## MakeHuman
https://www.makehumancommunity.org/
Core asset license: https://www.makehumancommunity.org/about/license.html

Useful as a no-cost character starting point.

---

# 7. Candidate benchmark — RETAIL / POS / DISPLAY
## Ten free candidates evaluated before selecting the stack


| # | Asset | Author | License | Link | Quality | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | POS Terminal – Digital Cash Register | dg samples | CC BY | https://sketchfab.com/3d-models/pos-terminal-digital-cash-register-dd3b0ff62c044d8ebe59c8cdab2c6fc9 | 4/5 | USE | Modern POS silhouette; good station donor. |
| 2 | Cash Register | BumBácBonifác | CC BY | https://sketchfab.com/3d-models/cash-register-1e04d7a73a004e2380e2ee715ce7bd06 | 4/5 | USE/DONOR | Detailed enough for close workstation use after re-materialing. |
| 3 | Cashier Machine – No Texture | YapGamedev | CC BY | https://sketchfab.com/3d-models/cashier-machine-no-texture-344514043f9b486bb9e90bfa05c4642a | 3.5/5 | DONOR | Clean geometry; specifically notes Unity support; requires proper materials. |
| 4 | Cash Register | hdyeah | Free Standard | https://sketchfab.com/3d-models/cash-register-bdfdda390b2b4632a32adda74853de85 | 3/5 | DONOR | High poly; shape useful but optimize and retexture. |
| 5 | Supermarket Checkout Counter | YaseminGungor | CC BY | https://sketchfab.com/3d-models/supermarket-checkout-counter-6d85fce1370f446e91c7c3568ed07813 | 2.5/5 | REFERENCE | Useful dimensions/components; wrong final counter shape and untextured. |
| 6 | Supermarket Checkout | rhcreations | CC BY | https://sketchfab.com/3d-models/supermarket-checkout-e750d80c13be46dca46d1eb8412770b3 | 3/5 | REFERENCE | Alternative checkout construction donor. |
| 7 | Display Case | chronickev | CC BY | https://sketchfab.com/3d-models/display-case-f0ab6595ba874a6ab6b3f40ca8935736 | 3.5/5 | DONOR | Good glass-case construction; far too many triangles for repeated use without optimization. |
| 8 | Animated Display Cabinet | anfang | CC BY | https://sketchfab.com/3d-models/animated-display-cabinet-938a9ba5180142818dfb0f50fe41f95c | 3/5 | DONOR | Unity-ready/opening parts; useful for interactive display logic. |
| 9 | ATM | AspectStudios | CC BY | https://sketchfab.com/3d-models/atm-a4216f71ffa74df9995b7feda1ae8ee7 | 4/5 | USE/DONOR | Good basis for entry ATM; retexture screen/body to match reference. |
| 10 | Handheld Barcode Scanner with Keypad | Cygnos | CC BY | https://sketchfab.com/3d-models/handheld-barcode-scanner-with-keypad-79d132dc44b344f7a019921e1b31c1b6 | 4/5 source | RETOPO/DONOR | High-detail scan; strong source for inventory scanner, but needs optimization. |


### Retail decision

**CUSTOM MODEL:**
- exact register run
- exact deli counter
- exact low glass case footprint
- queue stanchions if the free models do not visually match
- jar-wall cabinetry
- living-wall frame
- merchandise-wall structures

**FREE DONOR HARDWARE:**
- POS Terminal by dg samples
- Cash Register by BumBácBonifác
- AspectStudios ATM
- chronickev case construction as reference
- custom card reader / receipt printer from simple Blender modeling if no free candidate matches

Why: the **counter geometry**, not the electronics, is what visually identifies this store.

---

# 8. Candidate benchmark — CANNABIS / DELI / ACCESSORIES
## Ten free candidates evaluated


| # | Asset | Author | License | Link | Quality | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Weed Bud | Shanti | CC BY | https://sketchfab.com/3d-models/weed-bud-bfeabeb5adff45b79d3b3b543bb673d0 | 5/5 source | PRIMARY HERO SOURCE | 250k triangles; retopologize and bake detail into several game-ready variants. |
| 2 | Rosenthal Cannabis Bud | weedconnoisseur | CC BY | https://sketchfab.com/3d-models/rosenthal-cannabis-bud-31e31bedfc974738950183b362be0273 | 5/5 source | SOURCE ONLY | Very dense scan; use for normals/material reference or aggressive retopo. |
| 3 | Weed Jar | AGW Entertainment | CC BY | https://sketchfab.com/3d-models/weed-jar-e8704d77ca1a41dda086aa064c6ee8ba | 4/5 source | REFERENCE/RETOPO | Cannabis-specific jar; ~1.1M tris is inappropriate for runtime. |
| 4 | Free Jar Pack | Yusuf | CC BY | https://sketchfab.com/3d-models/free-jar-pack-da8bc020664f4a3e99bad40f8a756134 | 4/5 | PRIMARY JAR DONOR | LOD0-2 and shared PBR atlases make this much more runtime-friendly. |
| 5 | CC0 – Jar | plaggy | CC0 | https://www.fab.com/listings/93812f6a-95ea-4c20-9f9b-7e0f7bb976e0 | 4/5 | USE/DONOR | Very light geometry and 4K PBR; excellent neutral jar base. |
| 6 | Cannabis Joint – Pre Rolled | woddson | CC BY | https://sketchfab.com/3d-models/cannabis-joint-pre-rolled-fc5daec8fc7f4fbf9424736fd4bcbdf0 | 3.5/5 | USE | Good low-cost pre-roll geometry. |
| 7 | Pink Goo 3x Cannabis Joint | Abdou_myj | CC BY | https://sketchfab.com/3d-models/pink-goo-3x-cannabis-joint-3d-model-vr-ar-8da23d9c61bd4920bde1523605d71906 | 3.5/5 | DONOR | Useful additional pre-roll variation. |
| 8 | Grinder Madera Cannabis | JMCerezo | CC BY | https://sketchfab.com/3d-models/grinder-madera-cannabis-b8b42636252f4831b9e0f73ba9c0b7d7 | 3.5/5 | MERCH USE | Good accessory/display prop. |
| 9 | Grinder | ghostnoface | CC BY | https://sketchfab.com/3d-models/grinder-3c18fb886dde484ea86b7bbb8b43c40d | 4/5 | MERCH/DONOR | Higher-detail alternate grinder. |
| 10 | Digital Scale | chronickev | CC BY | https://sketchfab.com/3d-models/digital-scale-a73f649778b14b6bbf40083b0fc1f1c8 | 4/5 | PRIMARY DELI PROP | 5.8k triangles; ideal base for the counter weighing workflow. |


### Cannabis/deli decision

The free cannabis pool is good enough if used intelligently.

#### Flower workflow
Create **5–10 optimized cannabis bud meshes** from the best CC BY scan sources:
- green dense
- green airy
- purple-heavy
- orange-pistil-heavy
- frosty/light
- darker compact

Target:
- hero bud LOD0: roughly 10k–30k tris
- medium LOD: 3k–8k
- distant jar filler: cards/impostors or extremely low-poly clusters

#### Deli jar system

Create one reusable Unity prefab:

```text
DeliJar
├── Glass
├── Lid
├── Label
├── FlowerVolume
│   ├── BudInstances
│   └── ShakeBottom
├── ScoopOrTongsAnchor
└── InteractionPoint
```

Data:
```text
strainName
brand
batch
pricePerGram
tier
inventoryWeight
maxWeight
fillLevel
budMeshSet
budMaterialSet
labelTexture
```

The **fill level should respond to gameplay inventory.** That single detail will make the deli wall feel far more real.

#### Cannabis product forms the store should support

Based on the current store/menu categories and typical CCTV product density:
- bulk/deli flower
- 3.5 g / 7 g / 14 g / 28 g bags or jars
- pre-roll singles
- pre-roll multipacks
- vape cartridges
- disposable/AIO vapes
- concentrate jars
- edible pouches
- edible tins/boxes
- tincture bottles
- topical jars/tubes
- batteries
- rolling papers
- cones
- grinders
- glass accessories

Most packaging should be **custom procedural packaging**, not downloaded one SKU at a time.

---

# 9. Candidate benchmark — BOH / FOH / HUB STORAGE & LOGISTICS
## Ten free candidates evaluated


| # | Asset | Author | License | Link | Quality | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Unity Warehouse | Unity Technologies Japan | Free Unity EULA | https://assetstore.unity.com/packages/3d/environments/industrial/unity-warehouse-276394 | 5/5 | PRIMARY LIBRARY | Photoreal HDRP; shelves, cargo, transport equipment, workers. |
| 2 | Cardboard Boxes Pack – Open with Separate Lids | Alex human | CC BY | https://sketchfab.com/3d-models/cardboard-boxes-pack-open-with-separate-lids-b9f45d235f47429891de472713feca94 | 5/5 utility | PRIMARY BOX SYSTEM | 100 real-world box sizes; separate lids; ideal for believable stock variation. |
| 3 | Metal Wire Shelf | Tsawodi | CC BY | https://sketchfab.com/3d-models/metal-wire-shelf-ef69cb7f369d47ba86e9a873b2401bfd | 4/5 | PRIMARY FOH/BOH RACK | Close visual family to the chrome wire racks in CCTV. |
| 4 | Metal Shelf Rack | Logan S. | CC BY | https://sketchfab.com/3d-models/metal-shelf-rack-fb263bf1610848a29e3a53fc443b7f6a | 3.5/5 | DONOR | Simple alternate metal shelf. |
| 5 | Garage Shelf | Yağız Solmaz | CC BY | https://sketchfab.com/3d-models/garage-shelf-8b3555c8083b4cb9a248feea44d186d6 | 4/5 | DONOR | High-detail steel shelf; optimize before repeating. |
| 6 | Warehouse Storage Racking | Lady Lion Studios | CC BY | https://sketchfab.com/3d-models/warehouse-storage-racking-fbx-low-poly-free-17cf3c10ae774006a0b93b79fbfdf109 | 3.5/5 | HUB DONOR | Useful larger-scale rack system. |
| 7 | Hand Truck | Mutanzom3D / Poly Haven | CC0 | https://polyhaven.com/a/hand_truck | 5/5 | USE | 8K source maps, realistic wear; excellent delivery/restock prop. |
| 8 | Worn Metal Rack | Luca B / Poly Haven | CC0 | https://polyhaven.com/a/worn_metal_rack | 5/5 | USE SELECTIVELY | High-end worn rack; best for HUB/service area rather than clean chrome FOH. |
| 9 | Plastic Crate 02 | Fabi_G / Poly Haven | CC0 | https://polyhaven.com/a/plastic_crate_02 | 5/5 | USE | Adjustable color; ideal for product/restock bins. |
| 10 | Plastic Container | PierreB3D / Poly Haven | CC0 | https://polyhaven.com/a/plastic_container | 5/5 | USE | Scuffed lidded tote; excellent visual match family for dense rear storage. |


### Storage decision

This is one of the strongest free categories.

The rear rooms can be built at very high quality with:
- Unity Warehouse
- Tsawodi wire shelf
- Alex human box system
- Poly Haven crates/totes/carts

Create procedural variations in:
- case size
- case label
- tape
- denting
- open/closed
- stack rotation
- missing boxes
- shelf fill
- blue/yellow tote color
- kraft bag piles

Do **not** hand-place every rear-room box.

---

# 10. Candidate benchmark — OFFICE / BREAK ROOM / RESTROOM / JANITORIAL
## Ten free candidates evaluated


| # | Asset | Author | License | Link | Quality | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | UnityJapanOffice | Unity Technologies Japan | Free Unity EULA | https://assetstore.unity.com/packages/3d/environments/unityjapanoffice-152800 | 5/5 | PRIMARY LIBRARY | Photoreal HDRP office; 102 models and large texture library. |
| 2 | Metal Office Desk | Ulan Cabanilla / Poly Haven | CC0 | https://polyhaven.com/a/metal_office_desk | 5/5 | DONOR | High-end desk; actual office L-desk should still be custom if proportions differ. |
| 3 | Basic Desk Bundle | Neomesh Studio | CC BY | https://sketchfab.com/3d-models/basic-desk-bundle-low-poly-free-d492f88bb51b4d9695cc2de205e7afa8 | 4/5 | DONOR | Monitor, keyboard, mouse, PC, mug and desk. |
| 4 | Office Desk | snaptoongames | CC BY | https://sketchfab.com/3d-models/office-desk-e0f8dc2f81d440a09e9519fdc9e74cb2 | 4/5 source | DONOR | High-detail office desk source. |
| 5 | Server Rack | Shalmon | CC BY | https://sketchfab.com/3d-models/server-rack-c144d837358d446998c7b63cd1bdf825 | 4/5 | PRIMARY IT RACK DONOR | Useful office/network detail visible in reference notes. |
| 6 | Coffee Maker | Fredrik Johansen | CC BY | https://sketchfab.com/3d-models/coffee-maker-9ccda2fddba846e6ba97eb774b8a09c6 | 4/5 | USE | Good break-room appliance. |
| 7 | Kitchen Appliances | Nicolai Kilstrup | CC BY | https://sketchfab.com/3d-models/kitchen-appliances-0b01a398fe1649aaacd6ebdf85bf5d6c | 3.5/5 | DONOR | Appliance donor for sink/fridge/etc.; use pieces, not full scene. |
| 8 | Modern Kitchen | ChoboiAssets | CC BY | https://sketchfab.com/3d-models/modern-kitchen-95163e53ab694ed6bcec1ae50158bc94 | 3.5/5 | DONOR | Microwave/fridge/cabinet proportions can be adapted. |
| 9 | Bathroom Supplies | CKModels | CC BY | https://sketchfab.com/3d-models/bathroom-supplies-ef9e5c199e704f6fb78d173c451ec18c | 3.5/5 | USE/DONOR | Small restroom objects. |
| 10 | Mop & Bucket FREE | LordSamueliSolo / Lady Lion Studios | CC BY | https://sketchfab.com/3d-models/mop-bucket-free-low-poly-0c5dce73a0504e2eb7544d2ec1f260c8 | 3/5 | JANITORIAL USE | Good enough for closet/background; retexture if necessary. |


### Additional free micro-assets for these rooms

- **Office Notepads — Ulan Cabanilla / Poly Haven**  
  https://polyhaven.com/a/office_notepads
- **Document File Folder — Kami Rapacz**  
  https://sketchfab.com/3d-models/document-file-folder-11390179bba7462484d344e2fe22c703
- **Clipboard with Pen — Kami Rapacz**  
  https://sketchfab.com/3d-models/document-clipboard-with-pen-8650234a2e7949ca9fe9b4124e000d97
- **Paper Stack — Vivify Productions**  
  https://sketchfab.com/3d-models/paper-stack-e8b337d31a5a44eaa7265c2dbc63fc1c
- **Wet Floor Sign — louis-muir**  
  https://sketchfab.com/3d-models/wet-floor-sign-d340f904c4684645a4e5282b5fbe963b
- **Toilet — CheBe**  
  https://sketchfab.com/3d-models/toilet-e6f4406e4b0b44a99ab2e3c10576b905
- **Modern Bathroom Assets — vixnik**  
  https://sketchfab.com/3d-models/modern-bathroom-assets-ee1d1fa20c24428b8369f56d76fe8660
- **Medical Supplies Collection — Miguel Adão** — useful for glove boxes / first aid / utility items  
  https://sketchfab.com/3d-models/medical-supplies-collection-eae9fc470e674c458791cf00b892340f

---

# 11. Candidate benchmark — SECURITY / LIFE SAFETY / IT
## Ten free candidates evaluated


| # | Asset | Author | License | Link | Quality | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Security Camera 01 | Alexander Otterbeck + Yann Kervran / Poly Haven | CC0 | https://polyhaven.com/a/security_camera_01 | 5/5 | PRIMARY CCTV | Rigged, weathered, 8K maps; excellent exterior/interior donor. |
| 2 | Security Camera 02 | Garrison Gager + Yann Kervran / Poly Haven | CC0 | https://polyhaven.com/a/security_camera_02 | 5/5 | PRIMARY CCTV ALT | Different housing; useful exterior variation. |
| 3 | Security Cameras – Low Polygon Game Ready | Renend Studio | CC BY | https://sketchfab.com/3d-models/security-cameras-low-polygon-game-ready-d7ff3d89fcda42f189064a7b2eadabd1 | 4/5 | USE | Bullet + dome types; efficient. |
| 4 | CCTV Security Camera – Realistic | mustydigitals29 | CC BY | https://sketchfab.com/3d-models/cctv-security-camera-realistic-3d-model-df72ff3e971447aea65ebf04120a71c6 | 4/5 | DONOR | 4K PBR candidate. |
| 5 | Dome Camera FREE | MiguelRamos | CC BY | https://sketchfab.com/3d-models/dome-camera-free-ab8d2a64d3894deba9af23203ba0368d | 4/5 | USE | Good compact interior dome camera. |
| 6 | TV CCTV Monitor | Simon_M2099 | CC BY | https://sketchfab.com/3d-models/tv-cctv-monitor-2273be0837bc453b982dfb19d82c9cc0 | 4/5 | DONOR | Screen is easy to customize; useful CCTV workstation donor. |
| 7 | Access Lock System – Card + PIN | Meowdeler | CC BY | https://sketchfab.com/3d-models/access-lock-system-card-pin-c9f6e26d5dbb493f9998f6b4be1fbde2 | 4/5 | USE | Restricted-door hardware. |
| 8 | Heavy Duty Steel Safe with Digital Keypad | MK2468 | CC BY | https://sketchfab.com/3d-models/heavy-duty-steel-safe-with-digital-keypad-6fc5ead0c035452c9876e683b2d460c5 | 4/5 | USE/DONOR | Good office safe source; duplicate/resize to match two real safes. |
| 9 | Fire Extinguisher | Kantemir | CC BY | https://sketchfab.com/3d-models/fire-extinguisher-7fbd47c7e423461b86d599d30f4dfb33 | 4.5/5 | USE | 4K PBR, reasonable geometry. |
| 10 | Emergency Light | re1monsen | CC BY | https://sketchfab.com/3d-models/emergency-light-4324a9252b70446dbf37b80bfb43ee32 | 4/5 | USE | Commercial emergency light with emissive potential. |


### Additional life-safety details

- Fire alarm pull station — thelegocri  
  https://sketchfab.com/3d-models/fire-alarm-pull-station-5140mps-2-976c3f7c0a604ceb8a0605b700397449
- Smoke Detectors FREE — Lady Lion Studios  
  https://sketchfab.com/3d-models/smoke-detectors-free-low-poly-caa8b33766f94328a5fa9e6b8a684eca
- Exit Sign — Mohammad Rajabloo  
  https://sketchfab.com/3d-models/exit-sign-3d-model-free-79370d94bd6e4fc9a496de45b168f580
- Electrical Panel — back  
  https://sketchfab.com/3d-models/electrical-panel-54970d4284da4575a938d0bdfb6f021c

### CCTV implementation

The reference notes indicate a **17-feed camera wall**:
- 6 exterior
- 6 sales floor
- 5 back-of-house

Unity implementation:
- each real camera becomes an actual scene camera
- output to RenderTexture
- monitors use those RenderTextures
- feeds update at reduced rates unless viewed closely
- use low refresh (e.g. 5–15 fps) to mimic real security video and reduce GPU load
- add subtle time/date overlay, compression/noise and exposure differences per camera

This is both visually authentic and mechanically useful.

---

# 12. Candidate benchmark — CEILING / LIGHTING / BUILDING SERVICES
## Ten free candidates evaluated


| # | Asset | Author | License | Link | Quality | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Mounted Fluorescent Lights | Ulan Cabanilla / Poly Haven | CC0 | https://polyhaven.com/a/mounted_fluorescent_lights | 5/5 | PRIMARY BOH LIGHT | High-end commercial/industrial fluorescent donor. |
| 2 | Caged Hanging Light | Ulan Cabanilla / Poly Haven | CC0 | https://polyhaven.com/a/caged_hanging_light | 5/5 | DONOR | Good material/lighting reference, though not exact sales-floor globe. |
| 3 | Fluorescent Lamp/Light 4096px | Mark Peters | CC BY | https://sketchfab.com/3d-models/fluorescent-lamplight-4096px2-af6ccbb048594b848f2af232307cab60 | 4.5/5 | USE/DONOR | Detailed fixture with high-res textures. |
| 4 | Ceiling Fluorescent Light | Jimmy Johansson | CC BY | https://sketchfab.com/3d-models/ceiling-fluorescent-light-73e2c74174514f5b974cd58f74a0cfaa | 3.5/5 | USE BACKGROUND | Very efficient geometry. |
| 5 | Rooftop Ventilations / Air Conditioning Units | Oskar3D_ | CC BY | https://sketchfab.com/3d-models/rooftop-ventilations-air-conditioning-units-6dfa32e7ec614362a29fd950b87212ca | 4/5 | PRIMARY ROOF DONOR | Modular/game-ready rooftop service details. |
| 6 | Exterior Aircon Unit | Monsta3D / Poly Haven | CC0 | https://polyhaven.com/a/exterior_aircon_unit | 5/5 | USE | Clean + heavily weathered variants. |
| 7 | Utility Box 01 | James Ray Cock / Poly Haven | CC0 | https://polyhaven.com/a/utility_box_01 | 5/5 | USE | Exterior service-wall detail. |
| 8 | Utility Box 02 | James Ray Cock / Poly Haven | CC0 | https://polyhaven.com/a/utility_box_02 | 5/5 | USE | Alternate utility enclosure. |
| 9 | Ceiling Fan | Ulan Cabanilla / Poly Haven | CC0 | https://polyhaven.com/a/ceiling_fan | 5/5 asset | REFERENCE/OPTIONAL | Only use where reference supports it. |
| 10 | Air Conditioner – Free to Use | BlueOxel | CC BY-SA | https://sketchfab.com/3d-models/air-conditioner-free-to-use-4cd41303c780431890f8c6615e80f6cc | 4/5 | DONOR | Useful alternate HVAC detail if needed. |


### Ceiling decision

The **sales floor ceiling should be custom reconstructed**. Ceiling height, grid, camera placement, globe pendant spacing and vents have too much visual impact to approximate randomly.

Free assets should fill:
- fluorescent fixtures
- HVAC vents
- sprinkler heads
- smoke detectors
- cameras
- speakers
- conduit
- utility housings

### Sales-floor globe pendant

If a perfect free globe/brass pendant is not found, model it yourself. It is simple geometry:
- UV sphere / blown-glass globe
- brass/gold ring
- stem
- ceiling rose
- emissive bulb

A 20-minute custom model will match the reference better than a free lamp with the wrong silhouette.

---

# 13. Candidate benchmark — MATERIALS / SURFACE FIDELITY
## Ten free high-quality material candidates

All ten below are from **Poly Haven**, therefore **CC0**.


| # | Material | Author | Link | Best use | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1 | Marble Tiles | Charlotte Baglioni | https://polyhaven.com/a/marble_tiles | Sales-floor floor candidate | TEST FIRST |
| 2 | Marble 01 | Rob Tuytel | https://polyhaven.com/a/marble_01 | Alternate pale stone/marble source | TEST |
| 3 | Marble Mosaic Tiles | Amal Kumar | https://polyhaven.com/a/marble_mosaic_tiles | Small-area/tile variation source | REFERENCE |
| 4 | Concrete Floor | eye-candy.xyz | https://polyhaven.com/a/concrete_floor | BOH/HUB concrete | USE |
| 5 | Concrete Floor 01 | Rob Tuytel | https://polyhaven.com/a/concrete_floor_01 | BOH/HUB alternate | USE |
| 6 | Smooth Concrete Floor | Dimitrios Savva | https://polyhaven.com/a/smooth_concrete_floor | Cleaner service floor | USE |
| 7 | Asphalt Floor | eye-candy.xyz | https://polyhaven.com/a/asphalt_floor | Parking lot | USE |
| 8 | Asphalt 01 | Charlotte Baglioni / Dario Barresi | https://polyhaven.com/a/asphalt_01 | Parking variation | USE |
| 9 | Fine Grained Wood | Rob Tuytel | https://polyhaven.com/a/fine_grained_wood | Counter/cabinet donor | USE/RECOLOR |
| 10 | Oak Veneer 05 | Jenelle van Heerden | https://polyhaven.com/a/oak_veneer_05 | Retail wood fixture donor | TEST |


### Material rule

Do not accept the first visually similar floor texture.

For the retail tile:
1. match tile dimensions
2. match grout width
3. match veining frequency
4. match reflectance/roughness
5. compare under the reconstructed store lights
6. adjust albedo/roughness in Substance/Blender/GIMP if required

The CCTV floor reads as a **light stone/marble-pattern tile**, but surveillance compression alters contrast. Use the public interior imagery to refine the final material.

### Imperfection pass

Create your own free decal library from procedurally generated masks:
- tiny scuffs
- subtle dirt at wall/floor edges
- cart wheel marks
- glass fingerprints
- tape residue
- box scrapes
- worn door threshold
- asphalt patching
- subtle concrete discoloration

Keep it controlled. The store is operational, not abandoned.

---

# 14. Candidate benchmark — EXTERIOR / PARKING / SERVICE AREA / VEHICLES
## Ten free candidates evaluated


| # | Asset | Author | License | Link | Quality | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Modular Chainlink Fence | James Ray Cock / Poly Haven | CC0 | https://polyhaven.com/a/modular_chainlink_fence | 5/5 | PRIMARY FENCE DONOR | Excellent free industrial fence kit; recolor/modify toward green privacy treatment. |
| 2 | Chainlink Fence – Tileable | ChoboiAssets | CC BY | https://sketchfab.com/3d-models/chainlink-fence-tileable-397735ac4f5b4ac9a4b582576315d065 | 3.5/5 | ALTERNATE | Very efficient tileable fence. |
| 3 | Street Asset Pack | vmatthew | CC BY | https://sketchfab.com/3d-models/street-asset-pack-f3eb47d02e2e4ab290e66752fa354b48 | 4/5 | USE/DONOR | Traffic signs, barrier, cone, boxes, trash bags, hydrant, bin and poles. |
| 4 | Exterior Aircon Unit | Monsta3D / Poly Haven | CC0 | https://polyhaven.com/a/exterior_aircon_unit | 5/5 | USE | Excellent wall/service utility. |
| 5 | Rooftop Ventilations / AC Units | Oskar3D_ | CC BY | https://sketchfab.com/3d-models/rooftop-ventilations-air-conditioning-units-6dfa32e7ec614362a29fd950b87212ca | 4/5 | USE | Roof silhouette/detail. |
| 6 | Generic Passenger Car Pack | Comrade1280 | CC BY | https://sketchfab.com/3d-models/generic-passenger-car-pack-20f9af9b8a404d5cb022ac6fe87f21f5 | 3.5/5 | BACKGROUND VEHICLES | Ten generic cars; good density without real badges. |
| 7 | Lowpoly Generic SUV | mk2design | CC BY | https://sketchfab.com/3d-models/lowpoly-generic-suv-edc994ad28ed438cb365c0e0389ac177 | 3/5 | BACKGROUND/MIDGROUND | SUV silhouette matches common parking-lot mix. |
| 8 | Low-Poly Sedan Car | scailman | CC BY | https://sketchfab.com/3d-models/low-poly-sedan-car-aeb2699532b4402e8b75ec8888b800b9 | 3.5/5 | MIDGROUND | Interior/separate doors/wheels; useful near camera. |
| 9 | Hand Truck | Mutanzom3D / Poly Haven | CC0 | https://polyhaven.com/a/hand_truck | 5/5 | SERVICE AREA | Delivery/loading detail. |
| 10 | Utility Box 01 | James Ray Cock / Poly Haven | CC0 | https://polyhaven.com/a/utility_box_01 | 5/5 | SERVICE WALL | Small infrastructure detail that prevents empty exterior walls. |


### Exterior decision

**CUSTOM MODEL:**
- exact building footprint
- façade massing
- green stucco surfaces
- wood/slat sign panel
- storefront glazing/frames
- parapet
- entry geometry
- service-door locations
- sidewalk/curb relationship from reference

**FREE ASSETS:**
- vehicles
- fence parts
- HVAC
- utility cabinets
- traffic cone
- trash/service props
- hand truck
- plants
- asphalt materials

### Exterior night realism

The CCTV night feeds show:
- clipped highlights
- high-contrast pools of light
- vehicle headlight bloom
- dark asphalt
- utilitarian wall lights

Do **not** make the actual player view look like CCTV.  
Instead:
- render physically plausible night lighting
- apply degradation only to CCTV monitor feeds

---

# 15. Candidate benchmark — PLANTS / LIVING WALL
## Ten free candidates evaluated


| # | Asset | Author | License | Link | Quality | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Potted Plant 01 | Rico Cilliers / Poly Haven | CC0 | https://polyhaven.com/a/potted_plant_01 | 5/5 | USE | Photoreal indoor plant. |
| 2 | Potted Plant 02 | Rico Cilliers / Poly Haven | CC0 | https://polyhaven.com/a/potted_plant_02 | 5/5 | USE | Variation. |
| 3 | Potted Plant 04 | James Ray Cock / Poly Haven | CC0 | https://polyhaven.com/a/potted_plant_04 | 5/5 | USE | Variation. |
| 4 | Fern 02 | Rico Cilliers / Rob Tuytel / Poly Haven | CC0 | https://polyhaven.com/a/fern_02 | 5/5 | LIVING-WALL DONOR | Excellent foliage card/mesh donor. |
| 5 | Planter Box 01 | James Ray Cock / Poly Haven | CC0 | https://polyhaven.com/a/planter_box_01 | 5/5 | EXTERIOR USE | Hedge/planting base. |
| 6 | Ivy for Walls | arca_done | CC BY | https://sketchfab.com/3d-models/ivy-for-walls-b5e66f95a4de4cc19e68596f489eeaac | 5/5 source | SOURCE/OPTIMIZE | High poly; strong living-wall source after retopo/instancing. |
| 7 | Bush + Ivy Pack LOWPOLY | EFX | CC BY | https://sketchfab.com/3d-models/bush-ivy-pack-lowpoly-8013c47de07d4f96aa5d8b37f05eb4f6 | 3.5/5 | FILLER | Efficient secondary foliage. |
| 8 | Pothos Potted Plant | AllQuad | CC BY | https://sketchfab.com/3d-models/free-pothos-potted-plant-money-plant-e9832f38484f4f85b3f9081b51fa3799 | 4/5 | USE/DONOR | Good indoor/living-wall species family. |
| 9 | Aloe Vera in Pot | abgreiver | CC BY | https://sketchfab.com/3d-models/aloe-vera-in-pot-realistic-indoor-plant-3d-model-ce3e556b8cc74853b5534352a9f54ae1 | 4/5 | OPTIONAL | Useful indoor variation. |
| 10 | Cannabis Sativa Plant | Zbrojmistrz | CC BY | https://sketchfab.com/3d-models/cannabis-sativa-plant-ea31a5768c06457ea2fd67c3eb3458b8 | 4/5 | DECOR/REFERENCE | Cannabis-specific botanical prop; optimize as needed. |


### Living-wall decision

Do **not** use one large flat green-wall texture.

Build:
1. simple custom backing panel matching the real wall
2. 8–20 reusable foliage clusters
3. GPU-instanced/LOD foliage
4. controlled random rotation/scale
5. custom store lettering in front
6. optional pink/floral decorative elements where visible in public interior imagery

The wall is a hero landmark.

---

# 16. Candidate benchmark — CHARACTERS / NPC ANIMATION
## Ten free options evaluated


| # | Asset/system | Author | License | Link | Use | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | MakeHuman core assets | MakeHuman Community | Core assets CC0 | https://www.makehumancommunity.org/ | Character generation | PRIMARY BASE | Best zero-cost way to create multiple editable humans without relying on one fixed pack. |
| 2 | Human Basic Motions FREE | Kevin Iglesias | Free Unity EULA | https://assetstore.unity.com/packages/3d/animations/human-basic-motions-free-154271 | Animation | PRIMARY | Current free Unity pack; locomotion and everyday base motions. |
| 3 | Basic Character Animations FREE | Burak Uzun | Free Unity EULA | https://assetstore.unity.com/packages/3d/animations/basic-character-animations-free-409552 | Animation | USE | Unity 6/HDRP compatible; locomotion/emote basics. |
| 4 | KinemIQ Free Game Animations | KinemIQ + source authors | CC0 + CC BY | https://kinemiq.app/free-game-animations/ | 460 clips | PRIMARY LIBRARY | Walks, idles, sit/stand and many retargetable clips. |
| 5 | CMU Motion Capture Database | Carnegie Mellon Graphics Lab | Free for use; see terms | https://mocap.cs.cmu.edu/ | 2605 trials | SPECIAL MOTION SOURCE | Huge raw mocap source; requires cleanup/retargeting. |
| 6 | Mocap ATLAS Free Animations | Mocap ATLAS | Free collection | https://www.mocapatlas.com/collections/free-mocap-animations | Studio mocap | USE | Good professional motion source; verify per-download terms. |
| 7 | Joe – Realistic Human | Arjun P Krishna | CC BY | https://sketchfab.com/3d-models/joe-realistic-human-3d-model-2a108401fe5547409a3ad666b9b7d6b3 | 4/5 source | NPC DONOR | Game-ready topology; useful individual NPC. |
| 8 | Rigged T-Pose Human Male + Face Blendshapes | Mike Alger | CC BY | https://sketchfab.com/3d-models/rigged-t-pose-human-male-w-50-face-blendshapes-cc7e4596bcd145208a6992c757854c07 | 4/5 source | DONOR | Useful facial/rig source. |
| 9 | Human Male/Female Basemesh Rigged | Niclas | CC BY | https://sketchfab.com/3d-models/human-male-female-basemesh-rigged-64e56e3520b841dfbb9e9cc81e1fe26e | 3/5 | BASEMESH | Useful for variations/clothing work. |
| 10 | Man In Coat – Human Rigged | Saitam | CC BY | https://sketchfab.com/3d-models/man-in-coat-human-rigged-model-cd71038373d5427099a7970f1a1af2df | 3.5/5 | BACKGROUND NPC | Mixamo-rigged style donor. |


### Character decision

**Characters are the biggest free-only visual bottleneck.**

The environment can reach near-AAA quality for $0. The free pool of realistic, diverse, fully rigged hero people is much weaker.

Recommended solution:
- MakeHuman for body/base diversity
- Blender for clothing/hair cleanup
- high-quality free skin materials where license permits
- Unity Humanoid rig
- KinemIQ / Kevin Iglesias / CMU for motion
- reserve best-quality characters for nearby staff/customers
- lower-detail characters only beyond the immediate interaction area

### Required dispensary animation set

At minimum:
- neutral standing idle
- looking around
- phone idle
- talking with hands
- waiting/impatient
- walking
- entering/exiting
- queue shuffle
- inspect shelf
- lean toward counter
- hand ID/card
- receive card
- hand cash
- receive bag
- carry small bag
- carry cardboard case
- lift tote
- restock shelf
- open jar
- use scale
- scoop/tong motion
- bag product
- type at POS
- use mouse
- scan barcode
- count money
- sit/stand at office desk
- drink from cup
- open/close stockroom door

KinemIQ's free video-to-animation workflow is also useful: record your own reference motion and retarget it, which can solve highly specific budtender actions without purchasing mocap.

---

# 17. Candidate benchmark — AUDIO
## Ten free sources/sounds evaluated


| # | Asset/source | Author | License | Link | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | GDC 2026 Game Audio Bundle | Sonniss + contributing vendors | Royalty-free; no attribution | https://gdc.sonniss.com/ | PRIMARY PROFESSIONAL SOURCE | 7.47GB+ / 347+ files from professional libraries. |
| 2 | Sonniss GDC archive | Sonniss + vendors | See bundle license | https://sonniss.com/gameaudiogdc/ | PRIMARY ARCHIVE | Hundreds of GB across previous bundles; search for doors, HVAC, room tone, paper, vehicles, machinery. |
| 3 | Supermarket Ambience Sounds | Alex_Jauk | Pixabay Content License | https://pixabay.com/sound-effects/film-special-effects-supermarket-ambience-sounds-518582/ | USE | Retail ambience/cashbox/people. |
| 4 | Supermarket Ambience | rocketchicken / Freesound community | Pixabay Content License | https://pixabay.com/sound-effects/city-supermarket-ambience-17419/ | USE | Long field recording with scanners/cart/freezer hum. |
| 5 | Beeping at a Cash Desk | Soundscape_Leuphana / Freesound community | Pixabay Content License | https://pixabay.com/sound-effects/film-special-effects-20131119-beeping-at-a-cash-desk-zoomh6yx-87265/ | USE | Authentic barcode/cash-desk beep. |
| 6 | Store Scanner Beep | freesound_community | Pixabay Content License | https://pixabay.com/sound-effects/search/stores/ | USE | Short scanner UI/interaction sound. |
| 7 | Cash Register Open | Universfield | Pixabay Content License | https://pixabay.com/sound-effects/search/stores/ | USE | Drawer action. |
| 8 | Paper Bag SFX | Mrstokes302 | Pixabay Content License | https://pixabay.com/sound-effects/search/stores/ | USE | Bagging/hand-off layer. |
| 9 | Grocery Store Freezer Door | freesound_community | Pixabay Content License | https://pixabay.com/sound-effects/search/grocery/ | OPTIONAL | Fridge / BOH door layer. |
| 10 | Supermarket / grocery / trolley library search | Multiple Pixabay contributors | Pixabay Content License | https://pixabay.com/sound-effects/search/supermarkets/ | SOURCE POOL | Cart, checkout, PA, crowd and store ambience. |


### Audio target list

The game needs more than background music.

#### Sales floor
- HVAC bed
- room tone
- distant conversation
- shoe footsteps on tile
- stanchion belt/post bumps
- POS beeps
- card terminal beeps
- cash drawer
- receipt printer
- plastic/paper package handling
- glass case open/close
- jar lid
- deli scoop/tongs
- scale button/beep
- menu monitor electrical hum only if subtle

#### Office
- computer fan
- mouse/keyboard
- paper
- stapler
- printer
- money counter
- safe keypad / safe door
- chair movement

#### Break room
- refrigerator compressor
- microwave button / hum / beep
- sink water
- coffee maker
- cabinet doors

#### BOH/HUB
- cardboard
- tape
- tote lids
- wire shelf rattle
- cart wheels
- delivery door
- HVAC
- fluorescent room tone

#### Exterior
- distant Phoenix traffic
- parked-car door
- engine start
- footsteps concrete/asphalt
- occasional aircraft ambience if location/reference supports it
- wind
- utility/HVAC hum

---

# 18. Room-by-room master Bill of Assets

This is the section that was missing from the first report.

Legend:
- **CUSTOM** — model specifically from the real store reference
- **FREE** — use a sourced free asset
- **PROC** — procedural/variant system
- **DECAL/UI** — 2D/texture/screen work
- **VERIFY** — reference is incomplete; do not guess final geometry

## 18.1 Retail / sales floor

### Architecture
| Object | Method | Priority | Notes |
|---|---|---:|---|
| Outer walls | CUSTOM | Critical | Exact floor-plan footprint |
| Sales/back-room dividing wall | CUSTOM | Critical | Match arches/openings |
| Customer entry | CUSTOM | Critical | Match west-wall placement |
| East emergency exit | CUSTOM | Critical | Exact location from plan |
| Columns ×2 | CUSTOM | Critical | Position from plan |
| Ceiling | CUSTOM | Critical | Camera/light/HVAC placement |
| Floor tile | FREE material + custom UV/layout | Critical | Match pattern scale |
| Baseboards/trim | CUSTOM | High | Small but visible |
| Door trim | CUSTOM | High | Black/dark commercial finish |
| Storefront glass | CUSTOM + HDRP glass | Critical | Real thickness/reflections |

### Main retail fixtures
| Object | Method | Priority | Notes |
|---|---|---:|---|
| Register L/run | CUSTOM | Critical | Store identifier |
| Register partitions/stations | CUSTOM | Critical | Up to 12 |
| Deli counter | CUSTOM | Critical | Exact plan position |
| Deli jar wall north | CUSTOM | Critical | Cabinet + procedural jars |
| Deli jar wall east | CUSTOM | Critical | Same modular system |
| Display case | CUSTOM/DONOR | High | Match low counter case |
| Living wall backing | CUSTOM | Critical | Exact dimensions |
| Living wall foliage | FREE + PROC | Critical | Multi-cluster, not flat texture |
| Store lettering | CUSTOM | Critical | 3D lettering |
| Menu screen | FREE monitor + custom screen | High | Dynamic RenderTexture/UI |
| Merchandise wall | CUSTOM shelves + PROC inventory | High | Match reference density |

### Queue / customer area
- black queue stanchions — CUSTOM simple model
- black belts — CUSTOM
- floor queue layout — CUSTOM from CCTV
- ATM — FREE donor, retexture
- small signs — DECAL/UI
- accessible/entry signage — DECAL/UI
- trash receptacle — FREE
- possible benches/seating — VERIFY/reference-match

### Register workstation — per active station
- monitor
- monitor stand
- keyboard
- mouse
- POS terminal
- card terminal
- cash drawer
- receipt printer
- receipt roll
- scanner
- countertop mat
- small bag supply
- kraft/plastic exit bags
- pen
- tape
- disposable gloves where applicable
- small promotional sign
- cable bundle
- cable pass-through
- power strip below counter
- stool/chair where reference supports it
- trash bin beneath/near station

### Deli workstation
- digital scale — FREE
- strain jar — PROC
- lid — PROC
- flower buds — PROC
- shake at jar bottom — PROC
- scoop/tongs — CUSTOM simple model
- weigh boat/paper — CUSTOM
- small deli bag — PROC
- label — DECAL
- label printer — FREE/CUSTOM
- label roll — CUSTOM
- gloves / glove box — FREE
- cleaning/alcohol wipe container — CUSTOM/FREE
- waste cup/bin — CUSTOM
- counter tray — CUSTOM
- pen/marker — FREE
- hand-wash sink/faucet — CUSTOM/FREE donor
- paper towel dispenser — FREE/CUSTOM

### Product packaging families — procedural
Create a neutral geometry library:
- mylar pouch small
- mylar pouch medium
- mylar pouch large
- cardboard box narrow
- cardboard box wide
- pre-roll tube
- pre-roll carton
- vape box
- AIO/disposable box
- concentrate puck/jar
- edible pouch
- edible tin
- tincture dropper bottle
- topical jar
- topical tube
- battery package
- rolling paper box
- cone pouch/tube

Use **texture atlases and material variants** for SKU diversity.

### Ceiling / overhead
- globe pendants — CUSTOM
- recessed/utility lights — FREE/CUSTOM
- CCTV cameras — FREE
- fire sprinkler heads — CUSTOM simple
- smoke detector — FREE
- HVAC register — CUSTOM/FREE
- speaker — CUSTOM simple
- emergency/exit sign — FREE
- possible conduit — VERIFY

---

## 18.2 Hall

Observed/known:
- patterned tile continuation
- black doors
- employee/restricted signage
- corkboard/bulletin board
- printed notices
- leaf artwork/door graphic
- tight corridor

Assets:
- walls — CUSTOM
- floor — custom material/layout
- doors — CUSTOM or free donor reworked
- hinges/closer/handle — CUSTOM
- corkboard — FREE/CUSTOM
- pushpins — PROC
- notices — DECAL
- policy sheets — DECAL
- employee-only sign — DECAL
- leaf print — DECAL
- thermostat — CUSTOM/FREE
- outlet/switch plates — CUSTOM
- camera — FREE
- ceiling light — FREE
- sprinkler — CUSTOM
- baseboard — CUSTOM

---

## 18.3 Office

### Fixed
- exact room shell — CUSTOM
- L-shaped desk/work counter — CUSTOM
- shelving — CUSTOM/FREE donor
- black door — CUSTOM
- second white/service door if present — CUSTOM
- coat hooks — CUSTOM

### Electronics / financial
- monitor ×2 or as reference confirms — FREE
- laptop — FREE
- keyboard/mouse — FREE
- desktop tower — FREE
- printer — FREE donor
- money counter — CUSTOM unless a free high-quality model is found
- cash trays — CUSTOM
- safe ×2 — FREE donor + scale/material edits
- network/IT rack — FREE
- router/switch — FREE/CUSTOM
- network patch cables — PROC spline/cable system
- power strips — CUSTOM
- cords — PROC

### Paper/clutter
- paper trays
- printer paper
- folders
- clipboards
- binders
- daily logs
- inventory sheets
- pens
- sticky notes
- tape
- calculator
- deposit bags
- cash bands
- trash can + liner
- drink cup/water bottle
- personal bag/jacket
- wall procedures/posters

Do not arrange these symmetrically. The camera shows a used workspace.

---

## 18.4 Break room

### Fixed
- room shell — CUSTOM
- cabinet run — CUSTOM
- dark/black countertop — CUSTOM/material
- sink — FREE/CUSTOM
- faucet — FREE/CUSTOM
- bench — CUSTOM
- black door — CUSTOM
- janitor-closet door if in this room — VERIFY

### Appliances
- microwave — FREE
- coffee maker — FREE
- refrigerator — FREE donor
- optional kettle/toaster if reference confirms

### Clutter
- coffee cups
- coffee pods/filters
- sugar/sweetener
- paper towel roll
- dish soap
- sponge
- employee lunch containers
- beverage cans/bottles
- trash can
- trash liner
- coats
- bags
- wall labor posters/notices
- calendar
- magnets/notes if fridge supports them
- cleaning spray

---

## 18.5 FOH — floor restock

Primary visual target from CCTV:
- chrome wire shelving
- organized products
- bins/totes
- white fridge
- yellow-lid tote
- concrete/service floor

Assets:
- wire racks — FREE, match dimensions
- shelf casters/feet — donor/custom
- blue/yellow/black totes — FREE + recolor
- small product cases — PROC
- shelf labels — DECAL
- barcode labels — DECAL
- refrigerator — FREE
- rolling restock cart — FREE
- clipboard — FREE
- scanner — FREE
- trash — FREE
- door — CUSTOM
- overhead light — FREE
- CCTV — FREE
- outlet/switches — CUSTOM
- wall marks — subtle decals

---

## 18.6 BOH — backstock

Primary visual target:
- narrow working aisle
- cases stacked one side
- chrome wire racks / cased product other side
- kraft order bags
- high density

Assets:
- wire shelving — FREE
- cardboard boxes — PROC based on Alex human set
- open boxes — PROC
- tape — material/decal
- shipping labels — DECAL
- kraft bags — CUSTOM simple geometry + material
- folded kraft bags — PROC
- order labels — DECAL
- plastic totes — FREE
- shelf labels — DECAL
- cart — FREE
- hand truck — FREE
- box cutter — FREE/custom
- tape gun — FREE/custom
- manifests/paperwork — DECAL
- overhead fluorescent — FREE
- cameras — FREE
- door hardware — CUSTOM

---

## 18.7 HUB

Plan/reference:
- largest rear room
- deliveries/general storage
- entered from office
- exterior employee-only delivery door nearby
- desks/computers
- general storage

Assets:
- exact room shell — CUSTOM
- delivery door — CUSTOM
- desks — FREE/CUSTOM
- office chairs — FREE
- computers/monitors — FREE
- printer — FREE
- shelving — FREE
- pallets — Unity Warehouse/free
- cases — PROC
- totes — FREE
- rolling carts — FREE
- hand truck — FREE
- delivery paperwork — DECAL
- trash/recycling — FREE
- utility cabinets — FREE
- electrical panel — FREE
- CCTV — FREE
- fluorescent lights — FREE
- HVAC vent — FREE/CUSTOM
- floor markings — decals if reference supports them
- cable/conduit — PROC/custom

---

## 18.8 HUB 2

The room footprint is known, but direct camera/reference coverage is weaker.

Build accurately:
- walls
- door to HUB
- floor
- ceiling
- lighting

Populate conservatively with:
- shelving
- boxes
- totes
- pallets
- carts

**Do not invent distinctive machinery/furniture until a stronger reference exists.**

---

## 18.9 Restroom

Known dimensions, weak direct visual reference.

Build a believable standard commercial unisex restroom:
- commercial toilet
- sink
- faucet
- mirror
- soap dispenser
- paper towel dispenser
- toilet-paper dispenser
- trash can
- sanitary bin if appropriate
- grab bars
- door
- door closer
- vent
- ceiling light
- sprinkler
- outlet/GFCI
- wall/floor tile

Treat exact finishes as **VERIFY**.

---

## 18.10 Janitor closet

Known area: ~19.19 sq ft. Exact location/corner still uncertain.

Assets:
- mop bucket
- mop
- broom
- dustpan
- cleaning bottles
- gloves
- paper towel/toilet-paper stock
- trash bags
- wet floor sign
- small utility shelf
- wall hooks
- mop sink if reference confirms
- water heater/plumbing only if reference confirms

---

## 18.11 Exterior

### Custom architecture
- building mass
- wall openings
- façade
- parapet
- storefront
- employee-only delivery door
- service wall
- sidewalk shape
- curb geometry

### Parking/service dressing
- asphalt PBR
- crack/patch decals
- painted parking stripes
- yellow curb markings
- crosshatching
- wheel stops if reference confirms
- concrete sidewalk
- curb ramps
- traffic cone
- parked sedans
- parked SUVs
- delivery vehicle variation
- hedge
- green privacy fence/gate
- dumpsters/trash if reference confirms placement
- rooftop HVAC
- wall HVAC
- utility boxes
- electrical panel
- conduit
- hose bib
- exterior lights
- security cameras
- signs
- bollards if present
- litter only sparingly

---

# 19. Store-specific objects that should be custom-modeled

Even with a zero-dollar asset budget, these should **not** be substituted by generic free models:

1. Full measured building shell
2. Exterior façade
3. Entry/storefront
4. Register run
5. Deli counter
6. Jar-wall cabinetry
7. Main sales-floor glass case dimensions
8. Living-wall carrier/backing
9. Store lettering
10. Arches/openings
11. Hall/door layout
12. Break-room cabinet run
13. Office L-desk if no donor matches
14. FOH/BOH room geometry
15. HUB/HUB2 partitions
16. Queue layout
17. Globe pendant lights
18. Green/privacy fence treatment if generic chainlink does not match
19. store-specific wall signs
20. store-specific menu/UI screens

These are mostly simple architectural models. Their **accuracy matters more than topology complexity**.

---

# 20. Product-density system

The CCTV shows too much product to hand-author everything.

## Geometry pool

Create:
- 12 bag shapes
- 10 box shapes
- 6 jar shapes
- 5 pre-roll tube shapes
- 5 concentrate containers
- 5 vape/AIO shapes
- 4 tincture/topical shapes
- 4 accessory carton shapes

Then generate hundreds of SKUs from materials/textures.

## Shader/material variation

Per package:
- base color
- roughness
- metallic/foil
- normal
- label texture
- barcode texture
- small legal/warning strip
- optional holographic/foil mask

## LOD

Close:
- readable label
- modeled seam/lid

Mid:
- atlas texture
- simplified geometry

Far:
- extremely low-poly box/bag with baked label color

---

# 21. Packaging reference strategy for a private recreation

Because this is private at-home use, you can choose between:

### A. Fictionalized brands
Safest and easiest to organize.

### B. Reference-inspired brands
Use similar color/form language but create your own labels.

### C. Direct recreation for private visual fidelity
If you recreate labels from your own reference photos, keep them isolated in a `PrivateReference/` content folder. If the project is ever distributed, remove/review them first.

Recommended Unity content split:

```text
Assets/
  Environment/
  FreeThirdParty/
  CustomModels/
  ProceduralProducts/
  PrivateReference/
  Materials/
  Audio/
  Characters/
  UI/
```

---

# 22. Deli-flower graphics pipeline

## Source
Use the high-poly free cannabis scans only as source.

## Blender workflow
1. duplicate source
2. retopologize
3. UV unwrap
4. bake normal/AO from scan
5. preserve high-frequency trichome look in normal/roughness
6. create material masks for leaf/pistil/frost variation
7. build multiple clump arrangements
8. create LODs

## Unity
- HDRP Lit
- two-sided foliage only if required
- detail normal
- subsurface/transmission kept subtle
- instancing
- random rotation/scale
- no one-million-triangle bud meshes inside every jar

---

# 23. Lighting recipe

## Retail
- neutral-to-warm decorative globe lights
- cooler commercial fill
- bright product-wall illumination
- controlled display-case lighting
- no excessive bloom

## Back rooms
- cooler fluorescent/LED utility feel
- flatter lighting
- less cinematic contrast
- practical fixtures determine the look

## Exterior day
- strong Phoenix sun
- hard shadows
- bright sky
- subtle heat/dust look, not orange “desert filter”

## Exterior night
- security/building fixtures
- vehicle headlights
- parking-lot spill
- dark open asphalt
- storefront glow

### Important
The **CCTV image is not the target exposure**. It is the target for layout/object presence. The player camera should look like a high-end real-time scene; only security monitors get CCTV degradation.

---

# 24. Glass

The store contains significant glass:
- storefront
- display cases
- jars
- possible case shelves

Rules:
- give glass real thickness
- use correct IOR/refraction where affordable
- fingerprints/smudges as subtle decals
- do not make all glass perfectly invisible
- create separate clean and handled variants
- display case glass should reflect light fixtures but not become a mirror

---

# 25. Small-detail checklist

These details are disproportionately important:

### Retail
- register cables
- receipt paper edge
- label rolls
- power bricks
- monitor vents
- counter seam lines
- screw heads
- rubber feet
- countertop scuffs
- small signs
- bag stacks
- shelf-price labels
- jar labels
- jar lid threads/ridges
- shake at jar bottoms

### BOH
- tape seams
- shipping labels
- torn cardboard edges
- box dents
- tote scratches
- shelf casters
- rack clips
- bin labels
- manifests
- marker writing
- kraft-bag folds

### Doors/walls
- closer arm
- hinges
- latch
- strike plate
- push bar
- lock cylinder
- card reader
- outlet plates
- switch plates
- thermostat
- wall anchors
- conduit clips

### Ceiling
- sprinklers
- camera mounts
- smoke detector
- speaker
- HVAC registers
- cable penetration
- light trim

### Exterior
- asphalt repairs
- line paint wear
- curb paint
- wall penetrations
- pipe/conduit
- utility stickers
- roof flashing
- HVAC rust
- dirt at wall base
- tire marks

---

# 26. Free-only quality rules

Reject a free asset if:
- visibly stylized against the real scene
- obvious AI mesh/texture artifacts
- broken UVs
- bad normals
- wrong scale and difficult to repair
- giant triangle count with no useful detail
- baked lighting/reflections in albedo
- unclear source provenance
- extracted from another commercial game
- no usable license
- low-resolution texture on a hero prop
- unrealistic roughness

Accept high-poly source assets if:
- they are visually excellent
- license is valid
- you are willing to retopologize/bake them

---

# 27. Attribution ledger

Maintain a simple CSV/Markdown file:

```text
asset_name
author
source_url
license
download_date
modified
where_used
notes
```

For CC BY assets, this prevents future confusion.

Poly Haven CC0 assets do not require attribution, but recording source is still good practice.

---

# 28. Unity import / conversion pipeline

## Every downloaded model

1. Open in Blender first.
2. Check real dimensions.
3. Apply transforms.
4. Fix normals.
5. remove hidden/unnecessary meshes.
6. remove useless materials.
7. retopologize if necessary.
8. create UV2/lightmap UV if needed.
9. standardize naming.
10. export FBX or glTF.
11. import into Unity.
12. create HDRP materials.
13. create LODGroup.
14. create simple colliders.
15. create prefab.
16. add source/license metadata in prefab notes or project ledger.

### Naming

```text
ENV_Retail_RegisterRun_A
PROP_POS_Terminal_A
PROP_Deli_Scale_A
PROP_Deli_Jar_A
PROP_Box_Case_01
PROP_Tote_Blue_01
SEC_CCTV_Dome_A
FX_Decal_FloorScuff_01
NPC_Customer_Male_01
```

---

# 30. Recommended free stack — final selections

## Architecture
**CUSTOM in Blender from floor plan**

## Materials
**Poly Haven CC0**
https://polyhaven.com/

## Backstock/HUB
**Unity Warehouse — Unity Technologies Japan**
https://assetstore.unity.com/packages/3d/environments/industrial/unity-warehouse-276394

## Office
**UnityJapanOffice — Unity Technologies Japan**
https://assetstore.unity.com/packages/3d/environments/unityjapanoffice-152800

## Boxes
**Cardboard Boxes Pack – Alex human**
https://sketchfab.com/3d-models/cardboard-boxes-pack-open-with-separate-lids-b9f45d235f47429891de472713feca94

## Wire rack
**Metal Wire Shelf — Tsawodi**
https://sketchfab.com/3d-models/metal-wire-shelf-ef69cb7f369d47ba86e9a873b2401bfd

## Totes
**Poly Haven Plastic Crate 02 + Plastic Container**
https://polyhaven.com/a/plastic_crate_02  
https://polyhaven.com/a/plastic_container

## Flower
**Shanti Weed Bud source → custom retopo**
https://sketchfab.com/3d-models/weed-bud-bfeabeb5adff45b79d3b3b543bb673d0

## Jar
**Yusuf Free Jar Pack / plaggy CC0 Jar → custom deli variant**
https://sketchfab.com/3d-models/free-jar-pack-da8bc020664f4a3e99bad40f8a756134  
https://www.fab.com/listings/93812f6a-95ea-4c20-9f9b-7e0f7bb976e0

## Scale
**chronickev Digital Scale**
https://sketchfab.com/3d-models/digital-scale-a73f649778b14b6bbf40083b0fc1f1c8

## POS
**dg samples POS Terminal + BumBácBonifác Cash Register**
https://sketchfab.com/3d-models/pos-terminal-digital-cash-register-dd3b0ff62c044d8ebe59c8cdab2c6fc9  
https://sketchfab.com/3d-models/cash-register-1e04d7a73a004e2380e2ee715ce7bd06

## ATM
**AspectStudios ATM**
https://sketchfab.com/3d-models/atm-a4216f71ffa74df9995b7feda1ae8ee7

## CCTV
**Poly Haven Security Camera 01/02 + a free dome camera**
https://polyhaven.com/a/security_camera_01  
https://polyhaven.com/a/security_camera_02  
https://sketchfab.com/3d-models/dome-camera-free-ab8d2a64d3894deba9af23203ba0368d

## Security hardware
**Meowdeler access system + MK2468 safe**
https://sketchfab.com/3d-models/access-lock-system-card-pin-c9f6e26d5dbb493f9998f6b4be1fbde2  
https://sketchfab.com/3d-models/heavy-duty-steel-safe-with-digital-keypad-6fc5ead0c035452c9876e683b2d460c5

## Utility lighting
**Poly Haven Mounted Fluorescent Lights**
https://polyhaven.com/a/mounted_fluorescent_lights

## Exterior fence
**Poly Haven Modular Chainlink Fence**
https://polyhaven.com/a/modular_chainlink_fence

## HVAC
**Poly Haven Exterior Aircon + Oskar3D rooftop units**
https://polyhaven.com/a/exterior_aircon_unit  
https://sketchfab.com/3d-models/rooftop-ventilations-air-conditioning-units-6dfa32e7ec614362a29fd950b87212ca

## Living wall
**Poly Haven foliage + optimized Sketchfab ivy**
https://polyhaven.com/a/fern_02  
https://sketchfab.com/3d-models/ivy-for-walls-b5e66f95a4de4cc19e68596f489eeaac

## Characters
**MakeHuman + selected CC BY people**
https://www.makehumancommunity.org/

## Animation
**KinemIQ + Human Basic Motions FREE + CMU**
https://kinemiq.app/free-game-animations/  
https://assetstore.unity.com/packages/3d/animations/human-basic-motions-free-154271  
https://mocap.cs.cmu.edu/

## Audio
**Sonniss GDC bundles + Pixabay field recordings**
https://gdc.sonniss.com/  
https://pixabay.com/sound-effects/search/supermarkets/

---

# 31. Download priority

## Phase A — download immediately
1. Unity Warehouse
2. UnityJapanOffice
3. Poly Haven materials required for graybox
4. Poly Haven Security Camera 01/02
5. Poly Haven crates/totes
6. Poly Haven Hand Truck
7. Poly Haven fluorescent lights
8. Poly Haven fence / HVAC / utility boxes
9. Tsawodi metal wire shelf
10. Alex human box pack
11. Shanti cannabis bud
12. Yusuf jar pack
13. chronickev digital scale
14. POS terminal
15. ATM
16. safe/access reader
17. main plant assets
18. KinemIQ/Unity free animation packs
19. Sonniss audio bundle

## Phase B — only after architecture is accurate
- additional clutter
- alternate plants
- extra accessories
- secondary characters
- additional vehicles
- extra packaging donors

This avoids accumulating hundreds of assets before the real shell is correct.

---

# 32. Quality targets

## Hero assets
Used within ~1–2 m of player:
- 2K–4K textures where warranted
- correct roughness/normal behavior
- modeled silhouette details
- clean LODs
- readable labels where gameplay requires them

## Midground
- 1K–2K
- simplified geometry
- good material response

## Background
- 512–1K
- aggressive LOD
- atlased materials
- no unnecessary geometry

---

# 33. Performance strategy for this specific store

The building is small enough for very high quality. The risk is **object count**, not world size.

### Biggest draw-call risks
- product packages
- jars
- labels
- boxes
- plant leaves
- NPCs
- CCTV RenderTextures

### Solutions
- GPU instancing
- material atlases
- repeated mesh variants
- room occlusion
- LOD groups
- baked lighting/static geometry
- reduced CCTV refresh
- NPC LOD/culling
- procedural shelf population

---

# 34. Remaining reference gaps — not research gaps

The asset sourcing is now sufficiently comprehensive to build the game.

What remains unknown comes from **missing visual reference**, not from missing free-asset research.

## Still unresolved in the supplied plan/reference
- Which of FOH/BOH is exactly ~163 sq ft versus ~180 sq ft
- Exact janitor-closet corner/position
- Which register is Register 1 / exact station numbering
- Exact ceiling height(s)
- Exact ceiling-grid dimensions
- Exact sales-floor light count/spacing
- HUB2 interior appearance
- Full restroom appearance
- Janitor closet interior
- Some office wall/equipment details hidden from cameras
- Full exterior on every side
- roof layout
- exact parking stall dimensions/count outside camera framing
- precise façade dimensions/elevations
- precise storefront frame/glass dimensions
- exact living-wall dimensions/depth
- exact deli jar dimensions/label design
- exact register/deli countertop heights and depths
- exact rear-rack dimensions

### How to handle these now
Do **not** invent them aggressively.

Use:
- floor-plan dimensions where available
- standard commercial dimensions as temporary graybox values
- obvious CCTV proportions
- editable prefabs so measurements can be corrected later

---

# 35. What not to use

Reject:
- paid packs
- obviously low-poly cartoon packs for hero views
- generic “weed dispensary” environments with the wrong layout
- ripped GTA assets
- AI-generated geometry with visible artifacts
- one-million-triangle scans used directly at runtime
- generic luxury-showroom counters replacing the real counter
- random neon cannabis signs that are not in the reference
- excessive weed-leaf decoration
- excessive dirt/grunge
- cyberpunk color grading
- generic “stoner shop” aesthetics

The real store is a **working modern dispensary**, not a head shop caricature.

---

# 36. Final art-direction rule

The most realistic version will not come from finding a magical free “dispensary pack.”

It will come from accurate reconstruction plus mundane detail:

- the right floor dimensions
- the right wall openings
- the right counter geometry
- the right jar density
- the right shelving
- the right boxes
- the right cables
- the right door hardware
- the right ceiling services
- the right inventory disorder
- the right parking geometry
- the right light behavior

The visual hierarchy should be:

1. **Exact architecture**
2. **Exact major fixtures**
3. **Correct materials**
4. **Correct product density**
5. **Correct operational clutter**
6. **Correct lighting**
7. **NPC behavior**
8. **micro-wear**
9. **post-processing**

Not the reverse.

---

# 37. Final conclusion

## Can this be done at $0 asset cost?

**Yes.**

The free ecosystem is sufficient to produce a high-end result because:
- the building is small
- the exact architecture is better custom-modeled anyway
- Poly Haven supplies exceptional CC0 surface/prop quality
- Unity supplies two unusually useful free photoreal HDRP projects
- Sketchfab has legitimate cannabis-specific CC BY assets
- free mocap is abundant
- free professional audio is abundant

## What is the biggest compromise?

**Realistic hero humans**, followed by very specific branded package art.

Neither prevents the environment from looking excellent.

## Final production philosophy

> **Do not use a low-quality free asset merely because it is free.**
>
> If the correct object is simple, build it.
>
> If the object is complex and generic, source it.
>
> If it repeats, proceduralize it.
>
> If it defines the identity of the store, reconstruct it from reference.

That is the highest-quality zero-dollar route to making the finished scene feel like the real Phoenix dispensary rather than a generic cannabis-themed game.


---

# Appendix A — quick attribution / source ledger

The entries below are the free third-party assets specifically recommended in this report. Recheck the listing license at download time because marketplace terms/listings can change.


| Asset/library | Author | License | Source |
| --- | --- | --- | --- |
| Poly Haven library | Poly Haven contributors | CC0 | https://polyhaven.com/ |
| Unity Warehouse | Unity Technologies Japan | Unity Asset Store EULA / Free | https://assetstore.unity.com/packages/3d/environments/industrial/unity-warehouse-276394 |
| UnityJapanOffice | Unity Technologies Japan | Unity Asset Store EULA / Free | https://assetstore.unity.com/packages/3d/environments/unityjapanoffice-152800 |
| Weed Bud | Shanti | CC BY | https://sketchfab.com/3d-models/weed-bud-bfeabeb5adff45b79d3b3b543bb673d0 |
| Rosenthal Cannabis Bud | weedconnoisseur | CC BY | https://sketchfab.com/3d-models/rosenthal-cannabis-bud-31e31bedfc974738950183b362be0273 |
| Weed Jar | AGW Entertainment | CC BY | https://sketchfab.com/3d-models/weed-jar-e8704d77ca1a41dda086aa064c6ee8ba |
| Free Jar Pack | Yusuf | CC BY | https://sketchfab.com/3d-models/free-jar-pack-da8bc020664f4a3e99bad40f8a756134 |
| CC0 Jar | plaggy | CC0 | https://www.fab.com/listings/93812f6a-95ea-4c20-9f9b-7e0f7bb976e0 |
| Cannabis Joint – Pre Rolled | woddson | CC BY | https://sketchfab.com/3d-models/cannabis-joint-pre-rolled-fc5daec8fc7f4fbf9424736fd4bcbdf0 |
| Pink Goo 3x Cannabis Joint | Abdou_myj | CC BY | https://sketchfab.com/3d-models/pink-goo-3x-cannabis-joint-3d-model-vr-ar-8da23d9c61bd4920bde1523605d71906 |
| Grinder Madera Cannabis | JMCerezo | CC BY | https://sketchfab.com/3d-models/grinder-madera-cannabis-b8b42636252f4831b9e0f73ba9c0b7d7 |
| Grinder | ghostnoface | CC BY | https://sketchfab.com/3d-models/grinder-3c18fb886dde484ea86b7bbb8b43c40d |
| Digital Scale | chronickev | CC BY | https://sketchfab.com/3d-models/digital-scale-a73f649778b14b6bbf40083b0fc1f1c8 |
| POS Terminal | dg samples | CC BY | https://sketchfab.com/3d-models/pos-terminal-digital-cash-register-dd3b0ff62c044d8ebe59c8cdab2c6fc9 |
| Cash Register | BumBácBonifác | CC BY | https://sketchfab.com/3d-models/cash-register-1e04d7a73a004e2380e2ee715ce7bd06 |
| Cashier Machine – No Texture | YapGamedev | CC BY | https://sketchfab.com/3d-models/cashier-machine-no-texture-344514043f9b486bb9e90bfa05c4642a |
| Display Case | chronickev | CC BY | https://sketchfab.com/3d-models/display-case-f0ab6595ba874a6ab6b3f40ca8935736 |
| Animated Display Cabinet | anfang | CC BY | https://sketchfab.com/3d-models/animated-display-cabinet-938a9ba5180142818dfb0f50fe41f95c |
| ATM | AspectStudios | CC BY | https://sketchfab.com/3d-models/atm-a4216f71ffa74df9995b7feda1ae8ee7 |
| Barcode Scanner | Cygnos | CC BY | https://sketchfab.com/3d-models/handheld-barcode-scanner-with-keypad-79d132dc44b344f7a019921e1b31c1b6 |
| Metal Wire Shelf | Tsawodi | CC BY | https://sketchfab.com/3d-models/metal-wire-shelf-ef69cb7f369d47ba86e9a873b2401bfd |
| Metal Shelf Rack | Logan S. | CC BY | https://sketchfab.com/3d-models/metal-shelf-rack-fb263bf1610848a29e3a53fc443b7f6a |
| Garage Shelf | Yağız Solmaz | CC BY | https://sketchfab.com/3d-models/garage-shelf-8b3555c8083b4cb9a248feea44d186d6 |
| Warehouse Storage Racking | Lady Lion Studios | CC BY | https://sketchfab.com/3d-models/warehouse-storage-racking-fbx-low-poly-free-17cf3c10ae774006a0b93b79fbfdf109 |
| Cardboard Boxes Pack | Alex human | CC BY | https://sketchfab.com/3d-models/cardboard-boxes-pack-open-with-separate-lids-b9f45d235f47429891de472713feca94 |
| Basic Desk Bundle | Neomesh Studio | CC BY | https://sketchfab.com/3d-models/basic-desk-bundle-low-poly-free-d492f88bb51b4d9695cc2de205e7afa8 |
| Server Rack | Shalmon | CC BY | https://sketchfab.com/3d-models/server-rack-c144d837358d446998c7b63cd1bdf825 |
| Coffee Maker | Fredrik Johansen | CC BY | https://sketchfab.com/3d-models/coffee-maker-9ccda2fddba846e6ba97eb774b8a09c6 |
| Kitchen Appliances | Nicolai Kilstrup | CC BY | https://sketchfab.com/3d-models/kitchen-appliances-0b01a398fe1649aaacd6ebdf85bf5d6c |
| Bathroom Supplies | CKModels | CC BY | https://sketchfab.com/3d-models/bathroom-supplies-ef9e5c199e704f6fb78d173c451ec18c |
| Mop & Bucket | LordSamueliSolo / Lady Lion Studios | CC BY | https://sketchfab.com/3d-models/mop-bucket-free-low-poly-0c5dce73a0504e2eb7544d2ec1f260c8 |
| Security Camera 01 | Alexander Otterbeck + Yann Kervran / Poly Haven | CC0 | https://polyhaven.com/a/security_camera_01 |
| Security Camera 02 | Garrison Gager + Yann Kervran / Poly Haven | CC0 | https://polyhaven.com/a/security_camera_02 |
| Dome Camera | MiguelRamos | CC BY | https://sketchfab.com/3d-models/dome-camera-free-ab8d2a64d3894deba9af23203ba0368d |
| Access Lock System | Meowdeler | CC BY | https://sketchfab.com/3d-models/access-lock-system-card-pin-c9f6e26d5dbb493f9998f6b4be1fbde2 |
| Heavy Duty Steel Safe | MK2468 | CC BY | https://sketchfab.com/3d-models/heavy-duty-steel-safe-with-digital-keypad-6fc5ead0c035452c9876e683b2d460c5 |
| Fire Extinguisher | Kantemir | CC BY | https://sketchfab.com/3d-models/fire-extinguisher-7fbd47c7e423461b86d599d30f4dfb33 |
| Emergency Light | re1monsen | CC BY | https://sketchfab.com/3d-models/emergency-light-4324a9252b70446dbf37b80bfb43ee32 |
| Fluorescent Lamp | Mark Peters | CC BY | https://sketchfab.com/3d-models/fluorescent-lamplight-4096px2-af6ccbb048594b848f2af232307cab60 |
| Rooftop HVAC Units | Oskar3D_ | CC BY | https://sketchfab.com/3d-models/rooftop-ventilations-air-conditioning-units-6dfa32e7ec614362a29fd950b87212ca |
| Chainlink Fence Tileable | ChoboiAssets | CC BY | https://sketchfab.com/3d-models/chainlink-fence-tileable-397735ac4f5b4ac9a4b582576315d065 |
| Street Asset Pack | vmatthew | CC BY | https://sketchfab.com/3d-models/street-asset-pack-f3eb47d02e2e4ab290e66752fa354b48 |
| Generic Passenger Car Pack | Comrade1280 | CC BY | https://sketchfab.com/3d-models/generic-passenger-car-pack-20f9af9b8a404d5cb022ac6fe87f21f5 |
| Ivy for Walls | arca_done | CC BY | https://sketchfab.com/3d-models/ivy-for-walls-b5e66f95a4de4cc19e68596f489eeaac |
| Bush + Ivy Pack | EFX | CC BY | https://sketchfab.com/3d-models/bush-ivy-pack-lowpoly-8013c47de07d4f96aa5d8b37f05eb4f6 |
| Pothos Potted Plant | AllQuad | CC BY | https://sketchfab.com/3d-models/free-pothos-potted-plant-money-plant-e9832f38484f4f85b3f9081b51fa3799 |
| Cannabis Sativa Plant | Zbrojmistrz | CC BY | https://sketchfab.com/3d-models/cannabis-sativa-plant-ea31a5768c06457ea2fd67c3eb3458b8 |
| KinemIQ Free Game Animations | KinemIQ / source authors | CC0 + CC BY | https://kinemiq.app/free-game-animations/ |
| CMU Motion Capture Database | Carnegie Mellon Graphics Lab | Free-use terms | https://mocap.cs.cmu.edu/ |
| Human Basic Motions FREE | Kevin Iglesias | Free Unity EULA | https://assetstore.unity.com/packages/3d/animations/human-basic-motions-free-154271 |
| Sonniss GDC 2026 Bundle | Sonniss + vendors | Royalty-free bundle license | https://gdc.sonniss.com/ |


---

# PART II — CUSTOM ASSET PRODUCTION

# 38. CUSTOM-ASSET PRODUCTION PROGRAM

The remaining niche assets are not a reason to accept lower-quality free substitutes. They are a reason to **manufacture the missing assets ourselves with free tools**.

The custom-asset program has five production methods:

1. **PARAMETRIC / SCRIPTED BLENDER ASSET**  
   Best for regular hard-surface objects with known dimensions: counters, shelving modules, jars, packages, stanchions, vents, plates, signs and architectural modules.

2. **MANUAL BLENDER ASSET**  
   Best when visual matching requires judgment, irregular bevels, reference tracing or sculpted shaping.

3. **PHOTOGRAMMETRY → RETOPOLOGY → BAKE**  
   Best when the user can photograph a real object and geometric/material fidelity matters.

4. **PROCEDURAL RUNTIME ASSET SYSTEM**  
   Best when hundreds of visual variants are needed: packaged products, box stacks, jar fill, labels, clutter, living-wall foliage and cable routes.

5. **2D / MATERIAL / DECAL ASSET**  
   Best for signs, labels, notices, screens, stickers, barcodes, warning text, grime, scuffs and graphics.

The goal is **not** “model everything manually.” The goal is to choose the cheapest production method that preserves fidelity.

---

# 39. FREE SOFTWARE TOOLCHAIN

No paid application is required by this plan.

| Discipline | Free tool | Required role |
|---|---|---|
| Game engine | Unity Personal | Runtime, HDRP, gameplay, UI, physics, AI, audio, scenes |
| 3D modeling / UV / baking / rigging | Blender | Primary DCC and scripted model generator |
| Procedural PBR materials | Material Maker | Tile, painted metal, plastic, paper/cardboard, wear masks |
| Raster editing | GIMP | Texture cleanup, masks, photo preparation |
| Painting / graphics | Krita | Labels, decals, roughness masks, paintovers |
| Vector graphics | Inkscape | Signs, icons, shelf tags, labels, printable graphics |
| Photogrammetry | Meshroom / AliceVision | Optional reconstruction from photos |
| Character bases | MakeHuman / MPFB | Free human generation pipeline |
| Audio editing | Audacity | Foley cleanup, looping, EQ, normalization |
| Version control | Git | Project history, branches, worktrees |
| Large local binary storage | Git LFS where practical | Optional; hosting quotas depend on provider |
| Image conversion / automation | ImageMagick / Python/Pillow | Batch texture processing |
| Scripting | Python | Blender generation, asset manifests, validators |
| IDE/editor | VS Code / VSCodium or editor of choice | C#, Python, Markdown, JSON |
| Build automation | Unity batch mode + shell/PowerShell | Compile/test/build automation |

## Tool rule

A worker must not introduce a paid dependency when a free route exists without getting an explicit project decision from the Hub.

---

# 40. CUSTOM ASSET DECISION TREE

For every object:

```text
Is it store-identifying?
  YES → Custom model it from reference.
  NO  ↓

Is there a visually strong, legitimately free asset?
  YES → Download, normalize, re-material, optimize, prefab.
  NO  ↓

Is the shape regular/measurable?
  YES → Generate/model it in Blender, preferably parametrically.
  NO  ↓

Can it be reconstructed from photos?
  YES → Photogrammetry → retopology → bake.
  NO  ↓

Is it mostly graphic/surface information?
  YES → Create as texture/decal/UI.
  NO  ↓

Manual Blender model from reference.
```

A mediocre free asset is never the default fallback.

---

# 41. CUSTOM-ASSET MASTER BACKLOG

The tables below convert the room-by-room Bill of Assets into an actionable custom-production backlog.

## 41.1 Architecture and hero fixtures

| ID | Asset | Production method | Automation potential | Priority | Acceptance requirement |
|---|---|---|---|---|---|
| CA-ARCH-001 | Complete building shell | Blender from floor plan | High for wall extrusion; manual QA required | P0 | Room footprint agrees with plan; no guessed room shifts |
| CA-ARCH-002 | Exterior façade massing | Blender from references | Medium | P0 | Proportions and openings match available exterior imagery |
| CA-ARCH-003 | Front storefront framing/glass | Blender | High | P0 | Correct scale, mullions, door clearances, glass thickness |
| CA-ARCH-004 | West customer entry | Blender | Medium | P0 | Position agrees with plan/CCTV |
| CA-ARCH-005 | East emergency exit | Blender | Medium | P0 | Position agrees with plan |
| CA-ARCH-006 | Employee delivery/service door | Blender | Medium | P0 | Correct service-wall relationship |
| CA-ARCH-007 | Interior arches/openings | Blender | High | P0 | Align with retail/back-room geometry |
| CA-ARCH-008 | Retail columns | Blender | High | P0 | Correct plan coordinates and dimensions |
| CA-ARCH-009 | Ceiling/grid base | Blender | High | P0 | Editable height; supports fixtures/cameras/vents |
| CA-ARCH-010 | Baseboards/trim set | Parametric Blender | High | P1 | Modular, correct profile, no texture seams |
| CA-FIX-001 | Register run | Parametric Blender + manual match | Very high | P0 | Exact station spacing; modular up to 12 stations |
| CA-FIX-002 | Register station divider/module | Parametric Blender | Very high | P0 | Reusable and dimensionally tied to master register run |
| CA-FIX-003 | Main deli counter | Parametric Blender + manual match | High | P0 | Matches plan footprint and CCTV silhouette |
| CA-FIX-004 | Deli jar-wall cabinet module | Parametric Blender | Very high | P0 | Repeats cleanly; exact jar spacing configurable |
| CA-FIX-005 | Main glass display case | Blender | High | P0 | Real glass thickness; correct counter height/depth |
| CA-FIX-006 | Merchandise-wall shelving | Parametric Blender | High | P1 | Shelf spacing configurable; procedural product anchors |
| CA-FIX-007 | Living-wall backing/frame | Blender | High | P0 | Correct dimensions; accepts procedural foliage |
| CA-FIX-008 | Store lettering/logo geometry | Blender/Inkscape | High | P0 | Clean vector-derived geometry |
| CA-FIX-009 | Office L-desk | Blender | Medium | P1 | Fits room and camera proportions |
| CA-FIX-010 | Break-room cabinet run | Parametric Blender | High | P1 | Fits known wall dimensions; sink/appliance cutouts |
| CA-FIX-011 | Queue stanchion | Parametric Blender | Very high | P1 | Black post/belt proportions match CCTV |
| CA-FIX-012 | Exterior wood/slat sign panel | Parametric Blender | Very high | P0 | Correct panel rhythm and depth |
| CA-FIX-013 | Green/privacy-fence treatment | Blender + free donor | Medium | P1 | Matches CCTV color/opacity better than raw chainlink |
| CA-FIX-014 | Parking/curb geometry | Blender | High | P1 | Matches camera geometry; uses decals for paint |
| CA-FIX-015 | Globe pendant | Parametric Blender | Very high | P1 | Correct globe/brass silhouette and physical scale |

## 41.2 Deli / flower assets

| ID | Asset | Production method | Automation potential | Priority | Acceptance requirement |
|---|---|---|---|---|---|
| CA-DELI-001 | Canonical deli jar | Blender/free donor reconstruction | High | P0 | Correct scale, glass thickness and lid proportions |
| CA-DELI-002 | Jar lid | Parametric Blender | Very high | P0 | Independent open/closed state |
| CA-DELI-003 | Jar label carrier | Procedural mesh/material | Very high | P0 | Dynamic strain/price/batch fields |
| CA-DELI-004 | Flower bud LOD family | Retopo/bake from licensed free source | Medium | P0 | Multiple phenotypes; no runtime scan meshes |
| CA-DELI-005 | Jar flower-volume system | Unity procedural | Very high | P0 | Visible fill follows inventory weight |
| CA-DELI-006 | Bottom shake/crumb layer | Procedural mesh/material | High | P1 | Subtle and performance-safe |
| CA-DELI-007 | Deli scoop | Blender | High | P1 | Ergonomic believable hard-surface model |
| CA-DELI-008 | Deli tongs | Blender | High | P1 | Rig/open-close if used interactively |
| CA-DELI-009 | Weigh boat / paper | Parametric Blender | Very high | P1 | Several sizes; bend/variation optional |
| CA-DELI-010 | Small deli bag | Blender + cloth-like shape keys | High | P0 | Empty/filled variants |
| CA-DELI-011 | Label roll | Parametric Blender | Very high | P1 | Separate roll/core and printable label strip |
| CA-DELI-012 | Label-printer shell if donor fails | Blender | Medium | P1 | Correct counter footprint |
| CA-DELI-013 | Glove box | Parametric Blender + texture variants | Very high | P2 | Simple product clutter |
| CA-DELI-014 | Waste cup/container | Blender | High | P2 | Counter-scale background realism |
| CA-DELI-015 | Handwash sink/faucet adaptation | Blender/donor edit | Medium | P1 | Fits real wall/counter placement |

## 41.3 Register / customer-facing micro-assets

| ID | Asset | Method | Automation | Priority | Requirement |
|---|---|---|---|---|---|
| CA-POS-001 | Counter cable grommet | Parametric Blender | Very high | P2 | Reusable |
| CA-POS-002 | Cable bundles | Unity splines / Blender curves | Very high | P1 | Controlled randomness; no spaghetti intersections |
| CA-POS-003 | Receipt roll | Parametric Blender | Very high | P2 | Used/new variants |
| CA-POS-004 | Counter mat | Parametric Blender | Very high | P2 | Rubber roughness |
| CA-POS-005 | Bag stack | Procedural mesh | High | P1 | Natural imperfect stack |
| CA-POS-006 | Tip jar if reference supports | Blender | High | P2 | Only place if verified |
| CA-POS-007 | Small countertop sign holder | Parametric Blender | Very high | P1 | Dynamic insert graphic |
| CA-POS-008 | Customer ID/card prop set | Blender + textures | High | P1 | Fictionalized/private reference art |
| CA-POS-009 | Cash/card handoff anchors | Unity transforms | Very high | P1 | Animation alignment |
| CA-POS-010 | Stanchion floor anchors | Blender | High | P2 | If visible |

## 41.4 Product-package base library

The following are **base meshes**, not individual SKUs.

| ID | Base form | Method | Variants generated | Priority |
|---|---|---|---:|---|
| CA-PKG-001 | Mylar pouch S | Parametric Blender | 30+ materials | P0 |
| CA-PKG-002 | Mylar pouch M | Parametric Blender | 30+ | P0 |
| CA-PKG-003 | Mylar pouch L | Parametric Blender | 30+ | P0 |
| CA-PKG-004 | Stand-up pouch | Parametric Blender | 20+ | P1 |
| CA-PKG-005 | Narrow carton | Parametric Blender | 30+ | P0 |
| CA-PKG-006 | Wide carton | Parametric Blender | 30+ | P0 |
| CA-PKG-007 | Square carton | Parametric Blender | 20+ | P1 |
| CA-PKG-008 | Pre-roll tube | Parametric Blender | 20+ | P0 |
| CA-PKG-009 | Pre-roll multipack carton | Parametric Blender | 20+ | P1 |
| CA-PKG-010 | Vape cartridge box | Parametric Blender | 30+ | P0 |
| CA-PKG-011 | Disposable/AIO box | Parametric Blender | 30+ | P0 |
| CA-PKG-012 | Concentrate puck | Parametric Blender | 20+ | P0 |
| CA-PKG-013 | Concentrate carton | Parametric Blender | 20+ | P1 |
| CA-PKG-014 | Edible pouch | Parametric Blender | 30+ | P0 |
| CA-PKG-015 | Edible tin | Parametric Blender | 20+ | P1 |
| CA-PKG-016 | Tincture bottle | Blender | 15+ | P1 |
| CA-PKG-017 | Topical jar | Parametric Blender | 15+ | P1 |
| CA-PKG-018 | Topical tube | Blender | 15+ | P1 |
| CA-PKG-019 | Battery blister/carton | Blender | 10+ | P2 |
| CA-PKG-020 | Rolling paper box | Parametric Blender | 20+ | P1 |
| CA-PKG-021 | Cone pouch/tube | Parametric Blender | 15+ | P1 |
| CA-PKG-022 | Accessory blister card | Parametric Blender | 15+ | P2 |

## 41.5 BOH / logistics custom assets

| ID | Asset | Method | Automation | Priority |
|---|---|---|---|---|
| CA-BOH-001 | Kraft order bag | Blender | High | P0 |
| CA-BOH-002 | Folded kraft-bag stack | Procedural | Very high | P1 |
| CA-BOH-003 | Case/shipping label system | Inkscape/Python/UI | Very high | P0 |
| CA-BOH-004 | Inventory tote label | Procedural decal | Very high | P1 |
| CA-BOH-005 | Shelf-location label | Procedural decal | Very high | P1 |
| CA-BOH-006 | Manifest sheet family | Procedural graphic | Very high | P1 |
| CA-BOH-007 | Packing tape strip | Procedural material/decal | Very high | P2 |
| CA-BOH-008 | Open-box insert/divider | Parametric Blender | High | P2 |
| CA-BOH-009 | Cart/restock-bin anchors | Unity | Very high | P1 |
| CA-BOH-010 | Blue/yellow tote material variants | Material system | Very high | P0 |

## 41.6 Commercial-building micro-assets

| ID | Asset | Method | Automation | Priority |
|---|---|---|---|---|
| CA-BLD-001 | Door closer | Parametric Blender | Very high | P1 |
| CA-BLD-002 | Panic/push bar | Parametric Blender | Very high | P1 |
| CA-BLD-003 | Lever handle | Parametric Blender | Very high | P1 |
| CA-BLD-004 | Lock cylinder | Parametric Blender | Very high | P2 |
| CA-BLD-005 | Strike plate | Parametric Blender | Very high | P2 |
| CA-BLD-006 | Hinge family | Parametric Blender | Very high | P2 |
| CA-BLD-007 | Outlet plates | Parametric Blender | Very high | P1 |
| CA-BLD-008 | Switch plates | Parametric Blender | Very high | P1 |
| CA-BLD-009 | Thermostat | Blender | High | P1 |
| CA-BLD-010 | HVAC register | Parametric Blender | Very high | P1 |
| CA-BLD-011 | Sprinkler head | Parametric Blender | Very high | P1 |
| CA-BLD-012 | Ceiling speaker | Parametric Blender | Very high | P2 |
| CA-BLD-013 | Junction box | Parametric Blender | Very high | P2 |
| CA-BLD-014 | Conduit elbows/segments | Procedural curves | Very high | P1 |
| CA-BLD-015 | Cable/pipe wall clamps | Parametric Blender | Very high | P2 |
| CA-BLD-016 | Hose bib | Blender | High | P2 |
| CA-BLD-017 | Roof flashing/parapet caps | Parametric Blender | High | P1 |
| CA-BLD-018 | Utility stickers/labels | Decals | Very high | P2 |
| CA-BLD-019 | Parking stripe/crosshatch decals | Procedural texture | Very high | P1 |
| CA-BLD-020 | Curb paint material variants | Material/decal | Very high | P1 |

## 41.7 Signage, print and screen assets

| ID | Asset | Method | Dynamic? | Priority |
|---|---|---|---|---|
| CA-GFX-001 | Employee-only sign family | Inkscape/Krita | No | P1 |
| CA-GFX-002 | Exit/emergency graphics | Inkscape | No | P1 |
| CA-GFX-003 | Labor/procedure poster set | Inkscape | No | P2 |
| CA-GFX-004 | Bulletin-board notices | Procedural paper graphics | Yes/variants | P2 |
| CA-GFX-005 | Menu screen design | Unity UI | Yes | P0 |
| CA-GFX-006 | POS UI | Unity UI | Yes | P0 |
| CA-GFX-007 | CCTV time/date overlay | Shader/UI | Yes | P1 |
| CA-GFX-008 | ATM screen | Unity UI | Yes | P2 |
| CA-GFX-009 | Shelf tags | Procedural | Yes | P0 |
| CA-GFX-010 | Jar labels | Procedural | Yes | P0 |
| CA-GFX-011 | Package labels | Procedural | Yes | P0 |
| CA-GFX-012 | Barcodes | Procedural | Yes | P1 |
| CA-GFX-013 | Shipping labels | Procedural | Yes | P1 |
| CA-GFX-014 | Warning/legal text blocks | Procedural | Yes | P1 |
| CA-GFX-015 | Office forms/logs | Procedural | Yes | P2 |

---

# 42. CHATGPT / CLAUDE-CAPABLE ASSET GENERATION

A code-capable agent can create a large portion of the niche asset library by writing **Blender Python**, procedural texture code and Unity editor tooling.

## 42.1 Best targets for automatic Blender generation

High confidence:
- architectural walls
- counters
- shelves
- cabinetry
- jars
- lids
- boxes/cartons
- tubes
- pucks
- stanchions
- signs
- vents
- outlet/switch plates
- door hardware
- sprinkler heads
- ceiling speakers
- label rolls
- receipt rolls
- simple sinks/counter cutouts
- utility boxes
- parking curbs
- fence/slat modules

Medium confidence:
- bags/pouches
- cables
- folded paper/kraft stacks
- irregular clutter piles
- simple plants assembled from existing foliage cards

Low confidence without human reference review:
- realistic people
- highly irregular cannabis flower
- complex organic plants from scratch
- hero photogrammetry cleanup
- exact unknown geometry not visible in references

## 42.2 Generator rule

Every scripted asset generator must expose dimensions as parameters.

Example conceptual API:

```python
build_register_run(
    station_count=12,
    counter_height_m=...,
    counter_depth_m=...,
    station_width_m=...,
    corner_radius_m=...,
    panel_thickness_m=...,
    cable_grommets=True,
)
```

Never hard-code unexplained geometry into a one-off script if that dimension may later be corrected from better reference.

---

# 43. BLENDER GENERATOR STANDARDS

All generated models:

- use metric units;
- apply transforms before export;
- use predictable origin placement;
- face forward consistently;
- use real dimensions;
- use bevels appropriate to manufacturing;
- avoid razor-sharp edges;
- contain clean normals;
- avoid n-gons in deforming/critical shading areas;
- use sane material slots;
- include UV0;
- include UV2/lightmap UV where needed;
- generate LOD source meshes if repetitive;
- separate moving parts;
- use descriptive object names.

## Pivot standard

```text
Floor-standing prop: bottom center
Wall-mounted prop: back-center mounting point
Door: hinge axis
Drawer: slide origin
Jar lid: rotational center
Monitor/screen: base or mounting point
Package: bottom center
```

## Scale standard

1 Blender unit = 1 meter.

---

# 44. CUSTOM ASSET SPEC TEMPLATE

Every custom asset task must have a file in:

`/Docs/Assets/Specs/<ASSET_ID>.md`

Template:

*(Template written by DOC-001, AUDIT-001 B7/DEC-064: the original handoff left this block empty. It follows the packets and handoffs actually used in `Docs/Tasks/` and `Docs/Handoffs/`.)*

```markdown
# <ASSET_ID> — <name>

**Owner task:** <TASK_ID> · **Source type:** custom | generator | CC0 third-party (ledger row)

## References
<reference files + tiles/crops; confidence High/Med/Low; GAP ids for unknowns (never invent)>

## Dimensions
<w × d × h with units and source; Low-confidence values marked>

## Materials
<surface list, HDRP material notes>

## Build
<Blender generator/params or source file; LODs; colliders; pivot; scale 1 unit = 1 m>

## License / provenance
<LICENSE_LEDGER row or "custom"; ASSET_CACHE_MANIFEST entry if downloaded>

## Acceptance
<preview render / in-engine capture required; asset acceptance gate per STUDIO_OS §63>
```

# 45. PHOTOGRAMMETRY PLAN

Use photogrammetry only where a real object is available to photograph and the gain is substantial.

## Good candidates
- actual deli jar
- actual bag/package forms
- counter accessories
- scales
- store-specific small décor
- unusual storage containers
- employee equipment
- real surface materials if legally/practically accessible

## Capture
- even diffuse lighting
- 60–150 overlapping photos for small objects
- full 360° orbit where practical
- several elevation rings
- fixed focus/exposure
- textured/nonreflective temporary reference surface
- measurement reference in frame

## Processing
Meshroom/AliceVision → Blender:
- clean mesh
- orient/scale
- retopo
- UV
- bake normal/AO/albedo
- remove reconstruction noise
- generate LODs
- Unity import

Do not use raw scan geometry at runtime.

---

# 46. PROCEDURAL ASSET SYSTEMS

Procedural generation is mandatory for the following categories.

## 46.1 Package Generator
Inputs:
- package form
- dimensions
- material family
- label texture
- foil mask
- roughness
- color
- SKU identifier

Output:
- prefab/material variant
- LODs
- shelf-placement metadata

## 46.2 Deli Jar Fill Generator
Inputs:
- inventoryWeight
- maxWeight
- seed
- bud family
- color phenotype

Output:
- deterministic bud placements
- fill level
- shake layer
- visual inventory state

## 46.3 Shelf Population Generator
Inputs:
- shelf dimensions
- product pool
- density
- facing count
- disorder seed

Output:
- product arrangement
- gaps
- minor rotation/offset
- stock count metadata

## 46.4 BOH Case Stack Generator
Inputs:
- box families
- stack footprint
- height range
- seed
- label family

Output:
- believable stacks without intersections
- occasional open box
- tote/case mix

## 46.5 Living Wall Generator
Inputs:
- wall bounds
- foliage cluster library
- density map
- random seed
- exclusion region around letters

Output:
- instanced foliage
- variation
- LOD-ready clusters

## 46.6 Cable / Conduit Generator
Inputs:
- start/end anchors
- route points
- radius
- slack
- material

Output:
- curve mesh
- clips
- optional bundled cables

---

# 47. CUSTOM TEXTURE / DECAL FACTORY

Free tools:
- Inkscape
- Krita
- GIMP
- Material Maker
- Python/Pillow

Automate:
- barcodes
- generic regulatory labels
- strain labels
- shelf tags
- shipping labels
- inventory-location labels
- office forms
- receipt textures
- screen mockups
- warning stickers
- box labels

Use a scriptable template system so text and color can be regenerated from data.

---


---

# PART III — ASSET GOVERNANCE, VALIDATION & REFERENCE CONTROL

# 63. ASSET ACCEPTANCE GATE

A model is not “done” because it exists.

Checklist:
- [ ] real-world scale verified
- [ ] pivot correct
- [ ] transforms applied
- [ ] normals clean
- [ ] UV0 clean
- [ ] lightmap strategy valid
- [ ] materials HDRP-correct
- [ ] no missing textures
- [ ] texture resolution justified
- [ ] LODs appropriate
- [ ] collider appropriate
- [ ] naming standard followed
- [ ] source/license recorded
- [ ] reference comparison performed
- [ ] prefab created
- [ ] performance reasonable

---

# 73. FREE ASSET ACQUISITION WORKFLOW

For each external asset:

```text
Research
↓
Verify free price
↓
Verify license
↓
Verify author/source
↓
Download
↓
Hash source file
↓
Enter asset registry
↓
Open in Blender
↓
Normalize/optimize
↓
Export
↓
Import into Unity
↓
Create HDRP materials
↓
Create prefab/LOD/collider
↓
Reference-match review
↓
Accept or reject
```

A downloaded asset is **not automatically an approved production asset**.

---

# 74. LICENSE VERIFICATION WORKCELL

Because free marketplace listings can change, create a small verification task before bulk acquisition.

Worker output:
- asset name
- author
- exact URL
- license shown at time of download
- screenshot/text evidence if practical
- date
- restrictions
- approved use category

For CC BY:
- add attribution record.

For CC0:
- still record provenance.

---

# 75. REFERENCE INDEX SYSTEM

`REFERENCES_INDEX.md` should map physical areas to sources.

Example:

```text
AREA: Retail
- Floor plan p1
- CCTV R2C1–R2C5
- CCTV R3C2
- public interior ref IMG-...
- confidence: high

AREA: HUB2
- floor plan p2
- no confirmed direct camera
- confidence: low
- rule: conservative generic storage only
```

Every custom asset task cites reference IDs instead of saying “look at the screenshot.”

---

# 76. REFERENCE CONFIDENCE LEVELS

- **A — Direct measured/reference evidence**
- **B — Clearly visible but not measured**
- **C — Inferred from multiple sources**
- **D — Conventional placeholder only**

Final art should avoid visually distinctive **D-level** details.

---

# 87. BLENDER VALIDATORS

Python script checks:
- unapplied transforms
- non-manifold geometry where inappropriate
- missing UVs
- material-slot count
- naming
- dimensions
- origin
- triangle count
- hidden source meshes accidentally included
- export collection correctness

Worker runs validator before handoff.

---

# 88. CUSTOM ASSET GENERATOR TESTS

A generator is not done until tested across boundary values.

Example register generator:
- 1 station
- 6 stations
- 12 stations
- alternate station width
- corner section enabled/disabled

Package generator:
- minimum dimensions
- maximum dimensions
- all material families
- label texture absent/present

Jar fill:
- 0%
- 10%
- 25%
- 50%
- 75%
- 100%

---

# 89. ART DIRECTION GUARDRAILS

Reject changes that drift toward:
- head shop cliché
- neon cyberpunk
- generic luxury showroom
- cartoon marijuana imagery
- excessive green
- perfectly clean stockroom
- abandoned/grungy warehouse
- nightclub lighting
- random cannabis décor unsupported by reference

The visual target is:
**a real, busy, professionally operated dispensary with ordinary commercial infrastructure.**

---

# 90. “NO INVENTION” POLICY

Agents may use standard commercial assumptions only as **temporary placeholders** when a reference gap blocks progress.

Every such placeholder must:
- be marked confidence D;
- be documented in `KNOWN_GAPS.md`;
- remain easy to replace;
- not become the basis for other irreversible geometry.

---


---

# Asset-plan maintenance rule

Update this file for:
- new verified free sources;
- license changes;
- custom asset specs;
- room/object discoveries;
- generator standards;
- art acceptance criteria.

Do not add:
- gameplay implementation logs;
- agent transcripts;
- project milestone status;
- unrelated code architecture.

Those belong in the Master Plan, Migration Plan, Studio OS, or task/handoff files.
