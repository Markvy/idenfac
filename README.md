# Mark's submission for the Insight Data Engineering NASA fansite analytics challenge

Okay, what to say here?  This is a readme, so I should put something worth reading.  If you're on the Insight team and evaluating my sumission, then I suppose you already know what's in this repo.  But technically this is a public repository so it is vaguely concievable that someone stumbled on this thing for some other reason.  If this applies to you, then all I can tell you is that the rules are here: https://github.com/InsightDataScience/fansite-analytics-challenge.

Okay, the instructions say to document dependencies and such, so let's start with that.  The whole thing is written in Python 2.7 and requires nothing beyond the standard library.  The run.sh file requires a POSIX shell (such as bash), but should be easy enough to port to Powershell or something if you're on Windows I suppose.  Because I was foolish enough to upload these things to github using their website rather than using git, run.sh is not marked as executable, and neither is run_tests.sh.  The Python should be portable across every major OS; the only things it does that need OS interaction are file I/O and checking the current time.  (Checking the current time is just used to print out how long the code took to run, so I could see if my optimizations were making things better or worse.)

Let's see, what else?  Maybe I can grumble a bit here.  I think that lexicographic order is a silly order for the hours.txt file, since its is both less useful than chronological order, and harder to code, and runs slower (and uses more memory).  Assuming all log entires occur during the same month, these are identical though.  Hm, might be worth adding a special case for that as a microptimization.  Would probably shave several seconds off the total runnning time.  Maybe I'll do that if I have time left over.  Maybe I'll even remember to update this readme.  Considering that I'm still writing this readme file and the deadline is awfully close, I probably won't get around to it.  I guess that's enough grumbling, though I really do think lexicographic order for the hours.txt file is silly.

Okay, let's talk tests.  I added one test in addition to the standard one.  It's called head10, because it's just the first 10 lines of the giant log file.  Is this a good test?  Well, one thing it does check is that hosts.txt is sorted properly, including breaking ties lexicographically.  Since the resources.txt file is sorted using the same algorithm, I'm pretty confident that this is also sorted properly.  But overall, it's not a great test.  For instance, it's basically impossible to compute hours.txt correctly for the standard test, and get it wrong for head10.  However, it's biggest virtue is that it's very easy to verify by hand.  A bigger test would be tedious to manually verify, and if my code failed, it would take some time to puzzle out whether my test is wrong, or my code has a bug.  But even with this excuse, it's not a great test.  For one thing, it doesn't exercise the logic for blocked.txt at all, which is arguably the most complicated feature in the entire challenge.  My code for this feature had 5 continue statements, by far the largest for any feature.  And as much as I'd like to claim that I don't make mistakes, I noticed a big one just yesterday: I was only blocking access to the login page, rather than the whole site.  Yikes.  Anyways, hopefully there's nothing else like that.

Might as well say a few words about how the code is organized.  Each of the four features is is implemented by a seperate Python program.  That is, hours.py is responsible for outputting hours.txt, hosts.py is responsible for hosts.txt, and so on.  This has some advantages and some drawbacks.  One nice thing is that the features are self-contained and can't possibly interfere with each other.  Another is that most of the code for each feature tends to fit on a single screen, even with a somewhat large font.  (Or at least, the code for the main loop fits on the screen, depending on how big your fonts are, or how small your screen is.)  I had originally hoped that I could tell bash to run each program in parallel, and since most machines have 4 cores, the total runtime would equal the runtime of the slowest program.  Alas, it seems I was too optimistic.  When running all 4 programs in parallel, they each seem to run almost twice as slowly as they do when run sequentially.  I'm not sure why the slowdown is this dramatic.  I'm pretty sure that it's not the fact that I'm quadrupling the amount of disk I/O.  The shell's time builtin says that the amount of user time spent when running all four in parallel exceeds the wall clock time of running all four sequentially, so there's clearly some overhead being introduced somewhere.  But even so, it's almost twice as fast as running them all sequentially.  Takes about 20 seconds on my machine.  One potential drawback of splitting all of them into seperate programs instead of having one giant program is that some redundant work has to be redone.  In particular, each program needs to do its own parsing.  For instance, hours.py and blocked.py both need to parse timestamps from the log.  Since parsing timestamps is fairly expensive, this sounds like a big deal.  In fact, it's not as bad as it sounds, because although hours.py needs the timestamp of every log entry, this is not true for blocked.py, which needs less than one percent of them.  Thus, the obvious optimization to apply to blocked.py is to only parse timestamps when there's no wait out.  And in fact, once this optimization is applied, parsing timestamps is no longer the bottleneck, and we can afford to use a slow parser just to save a few lines of code.  On the other hand, hours.py needs to parse them as quickly as possible.  (Come to think of it, I may have gone a bit too far in the direction of self contained programs if I'm using two different methods of parsing timestamps.)

And that's about it I guess.  I suppose I could attempt a code walkthrough, but mostly the implementation is just the first thing that would occur to someone after reading the spec.  In the case of hosts.py and resources.py, the algorithm is lierally "count and then sort".  In the few cases where there's a trick or two (like why I store negative numbers instead of positive numbers sometimes), there is usually a comment right next to it.  The code for blocked.py is not "count and sort"; instead it's just a bunch of tedious if-else statements that should be done in the right order for a mix of correctness and efficiency reasons.  (The efficiency comes mainly from striving to avoid parsing timestamps needlessly.)  In the case of hours.py, I did not end up using the first algorithm I thought of; that one turned out to be kind of messy.  Eventually I realized that I could once again use trusty old count-and-sort.  In this case, for every second, count how many events there that second.  The one twist is that before sorting, I need to aggregate things so we the count for each hour, rather than each second.

# The end
