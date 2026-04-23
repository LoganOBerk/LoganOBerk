<div align="center">

<!-- HEADER BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=LOGAN%20BERK&fontSize=72&fontColor=00FFD1&fontAlignY=38&desc=Backend%20%7C%20Systems%20%7C%20Architect&descSize=20&descAlignY=62&descColor=FF2D78&animation=twinkling" width="100%"/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=22&duration=3000&pause=800&color=00FFD1&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=60&lines=Design+the+architecture.+Then+write+the+code.;Correctness+is+a+feature%2C+not+an+afterthought.)](https://git.io/typing-svg)

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-logan--berk-0D1117?style=for-the-badge&logo=linkedin&logoColor=00FFD1&labelColor=0D1117&color=FF9500)](https://linkedin.com/in/logan-berk)

</div>

---

<div align="center">

## ⚡ `whoami`

</div>

```python
class LoganBerk:
    university   = "University of Michigan-Dearborn"
    degree       = "B.S. Computer Information Systems — CS Specialization"
    gpa          = 3.95
    graduation   = "Winter 2027"
    seeking      = "Backend / Systems Engineering Internship"

    philosophy   = [
        "Design structure before writing line 1",
        "Architecture and correctness are first-class requirements",
        "Runtime efficiency is non-negotiable",
    ]

    superpower   = "Sole architect on team projects — sets structure teammates can't break"
```

---

<div align="center">

## 📊 By the Numbers

<br/>

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=LoganOBerk&show_icons=true&theme=midnight-purple&bg_color=0D1117&title_color=00FFD1&icon_color=FF2D78&text_color=FFFFFF&border_color=00FFD1&border_radius=12&hide_border=false&rank_icon=github)
&nbsp;&nbsp;
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=LoganOBerk&theme=midnight-purple&bg_color=0D1117&title_color=00FFD1&text_color=FFFFFF&border_color=FF2D78&border_radius=12&layout=compact&langs_count=6)

<br/>

![GitHub Streak](https://streak-stats.demolab.com?user=LoganOBerk&theme=dark&background=0D1117&border=00FFD1&ring=FF2D78&fire=FF9500&currStreakLabel=BF5AF2&sideLabels=00FFD1&dates=888888&border_radius=12)

</div>

---

<div align="center">

## 🛠 Arsenal

**Languages**

![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=0D1117)
![C](https://img.shields.io/badge/C-6699CC?style=for-the-badge&logo=c&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)

**Frameworks & Tools**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-0F80CC?style=for-the-badge&logo=sqlite&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-6e40c9?style=for-the-badge&logo=github&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-BF5AF2?style=for-the-badge&logo=pandas&logoColor=white)

**Core Concepts**

![OOP](https://img.shields.io/badge/OOP-BF5AF2?style=flat-square&logoColor=white)
![Data Structures](https://img.shields.io/badge/Data%20Structures%20%26%20Algorithms-6A0DAD?style=flat-square&logoColor=white)
![System Architecture](https://img.shields.io/badge/System%20Architecture-FF2D78?style=flat-square&logoColor=white)
![Database Design](https://img.shields.io/badge/Database%20Design-FF9500?style=flat-square&logoColor=white)
![Concurrent Systems](https://img.shields.io/badge/Concurrent%20Systems-C2185B?style=flat-square&logoColor=white)

</div>

---

<div align="center">

## 🚀 Featured Projects

</div>

<br/>

### [EdgeXchange](https://github.com/LoganOBerk/edgexchange) &nbsp; `Mar 2026`

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat-square&logo=sqlite&logoColor=white)
![bcrypt](https://img.shields.io/badge/bcrypt-FF2D78?style=flat-square)
![ndjson](https://img.shields.io/badge/ndjson-BF5AF2?style=flat-square)

> Paper trading platform — buy and sell real stocks at live prices with zero risk, via CLI or web server.

I was the sole architect on a 4-person team. Before anyone wrote a line of business logic, I locked down **7 strict layers** in 3 days — sanitization, validation, service, persistence, integration, interface, and domain models. Teammates filled in logic without touching a single structural file.

- 🔐 **Auth** — bcrypt-secured login, in-memory session store, per-user threading locks for concurrent safety
- 📡 **Streaming** — live portfolio endpoint via ndjson at 1s intervals
- 🗄️ **Database** — SQLite with foreign-key constraints and atomic transactions

<br/>

---

### [A\* Puzzle Solver](https://github.com/LoganOBerk/8tilesolver) &nbsp; `Jan–Feb 2026`

![C++](https://img.shields.io/badge/C++-00599C?style=flat-square&logo=cplusplus&logoColor=white)
![A* Search](https://img.shields.io/badge/A*%20Search-FF2D78?style=flat-square)
![Custom Hashing](https://img.shields.io/badge/Custom%20Hashing-BF5AF2?style=flat-square)

> Finds optimal solutions to sliding tile puzzles, including wind-weighted move costs that make certain directions more expensive.

Every design decision was made to prevent a specific failure mode in naive A*. The state uses a dual representation for O(1) heuristic lookup. A polynomial hash functor handles collision resistance. FIFO tiebreaking keeps solutions deterministic. The abstract `Agent` base class means swapping in BFS, DFS, or Greedy requires implementing exactly one class — nothing structural changes.

- ⚡ **25% faster** runtime than naive implementations

| Component | Technique | Why |
|:---|:---|:---|
| State | Dual-representation (board + per-tile arrays) | O(1) heuristic lookup |
| Hashing | Polynomial `StateHash` functor | Collision-resistant |
| Tiebreaking | FIFO via insertion index | Deterministic, optimal |
| Agent | Abstract, algorithm-agnostic base class | Swap algorithms with zero structural changes |

<br/>

---

### [Date-Indexed Task Manager](https://github.com/LoganOBerk/taskmanager) &nbsp; `Jun–Aug 2025`

![C++](https://img.shields.io/badge/C++-00599C?style=flat-square&logo=cplusplus&logoColor=white)
![std::map](https://img.shields.io/badge/std::map-FF9500?style=flat-square)
![Custom Operators](https://img.shields.io/badge/20%2B%20Operators-BF5AF2?style=flat-square)

> CLI task manager organized by date — like a calendar planner — with automatic file persistence on exit and restore on launch.

The goal was to push all complexity into the data structures so the application layer stays clean. The `Date` class carries full calendar arithmetic — leap years, month rollover, 20+ overloaded operators — and serves as a first-class map key. `std::map<Date, TaskList>` keeps everything chronologically sorted with no extra logic. A custom case-insensitive hash functor means task lookups are always O(1) regardless of how the user typed the input.

- 🔤 **`CaseInsensitiveHash` + `CaseInsensitiveEqual`** — O(1) case-tolerant lookup by design
- 📅 **`Date` class** — 20+ operators: leap year normalization, month/day rollover, stream I/O
- 🗂️ **`std::map<Date, TaskList>`** — chronological order for free, no sorting logic anywhere

<br/>

---

<div align="center">

## 🎓 Education

</div>

<div align="center">

### University of Michigan-Dearborn

![Degree](https://img.shields.io/badge/B.S.%20Computer%20Information%20Systems-CS%20Specialization-0D1117?style=for-the-badge&labelColor=161B22&color=161B22)
![GPA](https://img.shields.io/badge/GPA-3.95-FF2D78?style=for-the-badge&labelColor=0D1117)
![Expected](https://img.shields.io/badge/Expected-Winter%202027-BF5AF2?style=for-the-badge&labelColor=0D1117)

<br/>

![DSA](https://img.shields.io/badge/Data%20Structures%20%26%20Algorithms-FF9500?style=flat-square&logoColor=0D1117)
![OS](https://img.shields.io/badge/Operating%20Systems-FF9500?style=flat-square&logoColor=0D1117)
![SWE](https://img.shields.io/badge/Software%20Engineering%20I-FF9500?style=flat-square&logoColor=0D1117)
![CompOrg](https://img.shields.io/badge/Computer%20Org%20%26%20Assembly-FF9500?style=flat-square&logoColor=0D1117)
![DiscMath](https://img.shields.io/badge/Discrete%20Mathematics-FF9500?style=flat-square&logoColor=0D1117)
![Net](https://img.shields.io/badge/Networking-FF9500?style=flat-square&logoColor=0D1117)

</div>

---

<div align="center">

## 💡 Highlights

| | |
|:---:|:---|
| 📦 | **3,000+ lines** of production-quality C++ across 5+ projects |
| ⚡ | Up to **40% runtime improvement** through targeted algorithm optimization |
| 🐛 | Surfaced **50+ bugs** across peer Java & Python codebases with root-cause analysis |
| 🏗️ | Designed **7-layer architecture** adopted by 4-person team in 3 days |
| 🔐 | Built concurrent, bcrypt-secured auth with thread-safe session management |

</div>

---

<div align="center">

## 📈 Activity

![Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=LoganOBerk&bg_color=0D1117&color=00FFD1&line=FF2D78&point=BF5AF2&area=true&area_color=FF2D7820&hide_border=false&border_color=00FFD1&radius=12)

<br/>

*"I design the system before I write the code."*

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

</div>
