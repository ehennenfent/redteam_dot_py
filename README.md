# redteam_dot_py
CS 460 project for gaining an unfair advantage during attack and defense CTF's

Basic architecture:
___
* attacks - interfaces for metasploit, bash, ssh, etc, that automate the steps of compromising a target machine
* data - enums and stored remote schema
* models - models for networks, including NAT and individual hosts
* tasks - background tasks for monitoring remote host uptime and executing local programs

Background:
___
This project was created to aid in red team exercises for Central Illinois High School Cyber Defense Competition (CIHSCDC) at ISU, although it should prove useful in other CTF's as well.
CIHSCDC involves an unbalanced red team vs blue team relationship. The blue teams are composed of the titular central illinois high school students. The red teams are composed of (relatively) experienced pentesters. Each group of students is given a network with a series of VMs to maintain. Each of the VM's is running a set of public-facing services, but unlike traditional A&D exercises, these services simply spit out the machine's flag. Students are not required to attack other teams; they are only graded on their ability to keep the service up, running, and displaying the flag as expected.
This meta changes the red team strategy in several ways. For the red team, compromising a box is no longer as simple as grabbing the flag and walking away. Depending on what the red team decides to do once they've gained access to the box, the students may need to counter their actions by replacing the flag, bringing services back online, or attempting to boot the red team off the box (thought not necessarily in that order). Thanks to the automated scoreboard, students can notice very quickly once their services stop functioning as intended, which means that red teams need to establish persistent access before breaking anything, and must actively battle with the blue team in order to maintain that access once they are detected. In practice, this means that without automation, the red team often ends up spending more time establishing persistence and pivoting within the networks of a few teams once they gain a foothold, which means that some teams do not receive as much attention as others, thus making the competition somewhat unfair.
Students are allowed to ask the administrators to reset their VM back to a fresh snapshot, at the cost of a few minutes of uptime. This means that the red team is effectively allowed to nuke boxes if they deem it necessary. Red teams are discouraged from doing this too frequently, as this would ruin the fun for the students, but occasional trolling is allowed.
When a box is reset, all of the red team's persistence mechanisms disappear, which can make it appear that the blue team has succesfully kicked them out. However, all the initial vectors of compromise are now available once again, which means that the red team must race against the blue team in order to re-compromise the host before the blue team can re-apply their security patches. As smart blue teams do their best to automate this patching, it is only logical for the red teams to do so as well.

Goals:
___
This project aims to give the red team a competitive advantage, and ensure equal coverage of various teams by doing three things:
* Monitoring the remote hosts to detect when a service goes down (red teams are not given access to the scoreboard),
* Detecting when a host briefly disappears and comes back, possibly indicating a reset (or reboot)
* Automatically re-compromising hosts after a reset
* Allowing the red team to rapidly apply an attack developed on one machine to all the machines on the network

Current state:
___
Working:
* Background tasks for polling remote services in a loop
* Detecting when a host goes down or comes back up
* Deploying attacks against all hosts
* Deploying attacks against hosts after they come back up

Future framework ideas:
* Metasploit integration - generic metasploit attack that allows one to attach a metasploit model to a host
* Nmap integration - automatically create network map from scan results
* Pre-built persistence modules

Usage instructions
___
This project is not intended to act as a one-stop-shop for CTF tools. Rather, new attacks should be developed during each CTF and dropped in the attacks directory.
First, the framework needs to understand the network topography. You can specify this by creating a .py file in data/engagements. The file should export a list of networks called `networks`. See `460_ad.py` for an example.
Next, run `python3 redteam.py` to start the interface. You can select a task in order to start it running in the background. Output is printed to `data.log.txt`. I suggest watching it via tail.
By default, the framework includes tasks to monitor the uptime of services. You can attach attacks to each host. If the host goes offline and comes back up, any attached attacks will be automatically re-run. As you develop new attacks against hosts, you can create python files for each of them in the attacks directory. See `ssh_attack.py` for an example.


Author's note: I wrote a lot of this code in a hurry right before the beginning of the CS 460 CTF, then refactored it to fit the intended structure after the fact. I haven't been able to test it quite as extensively post-refactor. Hopefully I didn't break anything.
