# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Core actions :
1. Create/ Add User (to Household)
2. Create/ Add Pet (to Household)
3. Create/ Add Tasks (to Household)

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
 Main idea:
 I envisioned this app to be a tool to serve at least one person, but with multi-person capability. The main design lives inside the class Household. The anatomy of household is straighfowards, Users and Pets live inside one in the code as well. In this Household at least at least one user needs to exist to managed at least one pet. 
    - User Class:
    The User class contains crucial info on user, personal info and schedule (the key driver of the app - time management), it is possible to add multiple people to a household, delete them, and for each on setup and manage their schedule and time they want to/ can dedicate to their Pet. 
    * extra functionality : If they run into scheduling issues they may ping another household user and request help

    - Pet Class:
    The Pet class contains crucial info on the household's pet. Pets can be created, added to a household and also removed - in case household is petsitting or even temporarily sheltering a pet. 

    - Task Class: 
    The Task class manages User-Pet tasks by engaging and extracting their data. It keeps track of scheduling, status and completion of each task.

    Supporting classes :
    * TaskLog Class: Supports accountability and tracking which tasks got done, when and by who. It can also support a future Analytics class.
    * Notification Class: It handles the ping operations, by sending, accepting or decling a ping by another household member. 
    * Scheduler Class: The key impact of this class is to facilitate decision making when user needs to ping someone - it allows user to see who is available to cover a shift if they run into a schedule conflict.



**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

 I had to make some iterations on how I wanted to handle Scheduling, initially I was conflicted over how it would be handled, I did not think it was reasonable for someone to assign household members a task in addition to their own task, or have multiple household members assign tasks to other household members, both of these solutions looked way too complex for a small project and also tedious, and even inconveninet, for a user to have so many responsibities. So I decided to instead come up with the 'ping' operation - keeping users responsibilities loosely coupled while allowing them to handle circumstances where they need to reschedule and request help from someone in the household. 
 
    User case 1 - Mary was supposed to walk her puppie, but she may need to pull extra hours at work, which means that she won't make it home on time to walk her puppy Lisa therefore she will ping her son Matt and her husband John and see who can walk their pet.

    User case 2 - Matt has a midterm exam he needs to study for, he was supposed to walk his puppy Lisa, but since he is too busy he will ping his older sisters who are coming home soon and see if any of them can walk the puppy. 
 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers the following constraints:

1. **Time availability** — Each user has an availability schedule (e.g., "Monday: 08:00-20:00") and tasks can only be assigned to users who are available at the scheduled time.

2. **Conflict avoidance** — The scheduler prevents two critical conflicts:
   - Same-pet conflicts: a pet cannot have two tasks at the same time
   - Same-assignee conflicts: a person cannot be assigned to two tasks at the same time

3. **Pet-task association** — Each task is linked to a specific pet, so tasks naturally separate by pet.

4. **Recurrence patterns** — Daily and weekly recurring tasks are automatically spawned at their next scheduled times.

**Priority decisions:**

I deliberately did **not** implement explicit task priority levels because:
- Most pet care tasks (walks, feeding, meds) are equally important for pet health
- Time-based sorting is sufficient for most households
- Adding priority levels would complicate the UI and decision-making without clear benefit

Instead, I chose to solve the **collaboration problem** — the ping system lets users dynamically handle conflicts by asking for help rather than having the scheduler enforce strict priorities.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

**Conflict Detection Performance:** My current implementation uses a linear O(n²) search to detect scheduling conflicts between tasks. While more optimized approaches exist (hash tables, indexed queries), I chose to prioritize **code readability and simplicity** over performance optimization. For the current scope (handling ~100 tasks per household), the linear search is sufficiently fast, and the straightforward logic is easier to understand, test, and maintain. This decision follows the principle that premature optimization often introduces unnecessary complexity. If the app scales to thousands of tasks per household, I would optimize using indexed lookups—but only when profiling reveals actual bottlenecks.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Claude and Copilot -- Ask, Agent, Plan modes. I also used Claude to generate a fun UI/ frontend and on top of testing BE, I asked Claude to generate a set of manual tests I could make to test if my app was actually working and iterated based on what worked and what didn't. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I ran into significant issues with my UI—AI kept generating bloated, spaghetti code. I considered pausing to review it, but it felt unreasonable that a simple Streamlit app had 2k lines at that point. I knew something was off, so I decided to start fresh with a new context window. This time, I defined my needs clearly upfront and added features incrementally instead of trying to build everything at once.

---

## 4. Testing and Verification

**a. What you tested**

I tested 69 critical behaviors across six core areas:

1. **Conflict Detection (16 tests)** — The most business-critical feature. I tested same-pet conflicts (two tasks for the same pet at the same time), same-assignee conflicts (same person double-booked), and edge cases like midnight boundaries and microsecond precision. These are important because a bug here could silently allow an impossible schedule (pet gets two baths at 8am).

2. **Recurring Task Execution (15 tests)** — I verified that daily and weekly recurring tasks spawn correctly with all properties inherited (pet, type, assignee, recurrence). Edge cases like leap years and month boundaries matter because missing these causes tasks to disappear or recur on wrong dates.

3. **Task Filtering & Queries (13 tests)** — Tested filtering by status (scheduled/completed), by pet, and by member. Important for usability—if filtering breaks, users can't see their tasks.

4. **Notification Workflow (12 tests)** — I validated the ping state machine: pending → sent → accepted/declined. Tested that timestamps are set correctly and that recipients can't double-accept. Critical because the entire collaboration feature depends on this.

5. **Task Sorting (9 tests)** — Verified chronological ordering works correctly, even with same-time tasks and microsecond differences. Users rely on correct ordering to understand their daily schedule.

6. **Integration Scenarios (5 tests)** — Cross-tested complex scenarios with 10+ recurring tasks plus conflicts. These catch bugs that only appear when features interact.

**Why these tests mattered:** Pet care tasks are recurring, time-bound, and multi-person—small bugs compound into major scheduling chaos. Testing at the unit level (individual features) plus integration level (features together) gave me confidence that the system works end-to-end.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

**Confidence: 4/5** — I'm confident the scheduler works correctly because I validated it with both automated and manual testing across 69 comprehensive tests. All tests pass, covering the core scheduling logic, recurring tasks, filtering, sorting, and the ping workflow.

**Edge cases I'd focus on with more time:**
- **Input validation:** Enforce string types for names and integer validation for phone numbers in forms
- **Multi-user interactions:** Test rapid ping responses and concurrent task updates from multiple household members
- **Notification edge cases:** Test scenarios like self-pinging, task deletion during an active ping, or message tampering

The main limitation is the lack of a persistence layer—I haven't tested data recovery or state consistency across app restarts.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with how I bridged the backend and frontend. It wasn't easy and required many iterations and sanity checks, but I'm proud I didn't give up on adding this level of polish to the overall product. Although my primary focus was getting the backend working, I knew from the beginning that I wanted this to be portfolio-ready, and I think I accomplished that goal.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would redesign the user onboarding flow to have users set up their availability schedules upfront, rather than just collecting email and phone. In hindsight, this was a missed opportunity to empower users to dynamically allocate and manage their own task capacity within the app. It's a feature that would have strengthened the product significantly.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that **documentation is critical for large projects**. There were moments where I felt overwhelmed and genuinely lost—I couldn't remember what I was trying to accomplish or how to improve something. Having my UML diagram, initial design notes, and project documentation as reference points was invaluable. In future projects, I'll invest extra time creating granular, well-organized documentation from the start to maintain continuity across all development stages.