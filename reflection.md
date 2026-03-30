# PawPal+ Project Reflection

## 1. System Design
User should be able to feed their pet, walk their pet, and buy toys.

**a. Initial design**

- Briefly describe your initial UML design.
There should be a pet owner class with actions like feeding pet, walking pet, and other actions. It will also have attributes like 
which pets the owner has, and personal identifiers if necessary. 
Pet class will belong to an owner, with attributes like species, name,  or other important pet details. Methods for pets will include actions like walking, etc.
Each task should have a description and name, as well as a method like to perform it or to mark it as complete. It is associated with pets.
The scheduler should have methods to add tasks and order them by deadline. It belongs to the owner

- What classes did you include, and what responsibilities did you assign to each?
I implemented all of these tasks, but instead assigned responsibilities like scheduling a walk to the scheduler class. The pet class doesn't have many methods other than just getting its daily needs. The tasks class has a name, description, and various other attributes like deadlines, with only a few methods like marking as complete or performing them. The scheduler handles a majority of the task related functions.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, the design changed during implementation, as I originally wanted to divide the the methods more evenly, but after receiving feedback, realized that it would be most efficient and make the most sense if I made it so that the majority of the tasks would be allocated to the scheduler class.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The scheduler considers the deadline for a task, its priority, and its name. First, the program prioritizes deadlines, like feeding a pet on time, then goes by priority, so feeding a pet would be more important than walking for example. Lastly, the name is a tiebreaker and just sorts the tasks alphabetically.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler scans every single task to check for time conflicts.
- Why is that tradeoff reasonable for this scenario?
This is reasonable because this program is not for production, and iterating through tasks won't take long.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI tools to scaffold the project and implement class features and functions.
- What kinds of prompts or questions were most helpful?
Prompts like "design a class based on this UML" were most helpful.
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
One moment where I didn't accept an AI suggestion was when it suggested adding an ID to each user. I rejected this because it would add unnecessary complexity, as this project is for one user only.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested the schedule conflicter logic, as well as general schedule making.
- Why were these tests important?
These tests were important because they are part of the main functionality of the app, and without a functioning schedule, the app is useless.
**b. Confidence**

- How confident are you that your scheduler works correctly?
I am very confident that the scheduler works correctly, though, I am a bit worried about whether one may confuse deadlines with the time to start a task vs finishing it.
- What edge cases would you test next if you had more time?
I would test what happens if you try to assign a task without having a pet, or what happens to pet if user is deleted.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with the scheduluer part of the project.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would make this project look more user friendly, and implement more features like reminders.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One thing I learned about designing systems and working with AI is that AI can be a powerful tool, but if you allow it to operate without checking in on it and making sure you know what it's doing, you may become lost in your own project, and be unable to solve issues that you didn't even know existed.