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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
