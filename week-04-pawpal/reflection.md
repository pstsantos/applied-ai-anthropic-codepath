# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Candidate classes 

1 - User

Attributes : main_ownerName, household_ownerName, phone (for texts/ notifications), email, hours available

// household_ownerName, in case a couple or a family of more than 1 decides to have a shared account, track other owners too.

Actions : 
- Add user (name, phone, email, and normalized schedule)
- Add household members
- Select main user 
- MixSchedules (optional // for household option)

2 - Pet

Attributes : petName, age, breed, vetName, vetPhone

Actions:
- Add Pet (petName, age, breed, vetName, vetPhone)
- Remove pet (in case you are temp hosting a pet)

3 - Tasks

Attributes : main_ownerName, household_ownerName, petName, feed, water, feedCount, waterCount, shortWalkCount, longWalkCount

Actions: 
- schedule walk (show who’s available)
- schedule Feed (show who’s available)
- schedule Water (show who’s available)
- schedule Appt (show who’s available)
- logFeed
- logWater
- logWalk
- logAppt
- seeTodaysTask

4 - Analytics 

Attributes : main_ownerName, household_ownerName, petName, feed, water, feedCount, waterCount, shortWalkCount, longWalkCount

Actions : 
- dietStatDailyAvg
- dietStatMonthAvg
- dietStatYearAvg
- exerciseStatDailyAvg
- exerciseStatMonthAvg
- exerciseStatYearAvg
- waterStatDailyAvg
- waterStatStatMonthAvg
- waterStatYearAvg
- medicineStat (optional)

Core actions :
1. Add Pet
2. Schedule walk
3. See today's tasks 

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
