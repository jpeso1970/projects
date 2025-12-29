# Participants

- Jeff Morton
- John Lavigne
- Josh (R365)
- Lucas Felak
- Paul Hurley

---

# Transcript

**Paul Hurley** (0:09): I was telling Jeff earlier that both my kids ended up getting the flu, so it was an intimate Thanksgiving, that's for sure. Put it that way.
**Lucas Felak** (0:20): Yeah, my wife was also sick, and my wife is one that when she is sick, she wants to tell us just how sick she is all the time.
**Paul Hurley** (0:31): Oh man, that's me. And I thought there was a guy thing. You know, that's me and my house.
**Lucas Felak** (0:37): No man, I suffer in silence. That is definitely that. I guess everyone's got one or another, right?
**Paul Hurley** (0:46): Yeah, yeah.
**Lucas Felak** (0:49): But yes, yeah, so.
**Paul Hurley** (0:50): That's funny.
**Lucas Felak** (0:50): OK. I'm glad. I'm glad everyone.
**Paul Hurley** (0:52): Yeah.
**Lucas Felak** (0:53): Or I'm glad it was intimate, at least. Whether or not it was enjoyable with two sick kids, I don't know.
**Paul Hurley** (1:00): Yeah, no, it ended up being fine. We just didn't travel. We planned on having our own thing on Friday, so it's not like we missed out on the turkey, the stuff like I had everything we needed. So we just accelerated that to Thursday instead and didn't travel. So it was all good.
**Lucas Felak** (1:18): Yeah. Sounds like, hey, Josh.
**Josh (R365)** (1:23): Hey everyone, so sorry about that. I had to restart my browser in order to get on Microsoft Teams.
**Lucas Felak** (1:29): Yes, I apologize for the fact that we are a Teams organization.
**Josh (R365)** (1:32): No, no worries.
**Lucas Felak** (1:32): It's not my favorite thing in the world, but it is what it is. Though I will say as I continue to use more and more automation in my life, having everything flow across a single ecosystem is enjoyable.
**Josh (R365)** (1:37): No worries at all.
**Lucas Felak** (1:50): That's for sure.
**Paul Hurley** (1:50): Yeah.
**Josh (R365)** (1:51): Oh, I bet, I bet.
**Lucas Felak** (1:51): Yeah, there's some cool new things coming out. Well, I will kick things off. I hope everyone had a lovely weekend. I hope the worst part of it was Paul's sick kids. But I appreciate everyone jumping on, and Jeff as well, and Josh getting introduced to you just in person here. The purpose of this call really is to make some of the introductions here about some of the discussions in the past that have been had and then also just get a better understanding from Quattro's US-based side, namely Jeff and I, on some additional ways that we are looking to increase some of the automation inside of Restaurant 365 without breaking anything, to be very, very...
**Josh (R365)** (2:21): Mm-hmm. OK, sounds good.
**Lucas Felak** (2:40): Clear. Yes. Yeah, so I would love to just kind of make sure that everyone's on the same page. Paul, do you have anything that you'd like to add on that front?
**Paul Hurley** (2:54): No, I think the only thing since we're all on the same page at the same time here, I think earlier on when we migrated onto our 365, I think we were under the impression with the salesperson that we were dealing with in our implementation team that a lot of the EDI capabilities, like in the, you know, were related to distribution vendors, right? So we were kind of advised early on, maybe because we were using CrunchTime, to just kind of stay away from any EDI implementation or integration with our distribution vendors and kind of just take information in from CrunchTime and bring it over the way we're doing it now. That's what we were initially told. It made sense at the time. I don't know, George, if anything like that doesn't make sense or whatever because that's kind of the way we went. And then I would say as far as other vendors, I would love to know what's out there, right? We have some really big vendors like Cintas, right? We do have a lot of really small, non-sophisticated vendors as well, power washing companies, landscapers, you know, more localized vendors that, of course, we're not gonna be able to really maybe get EDI going there. But anywhere where we can get efficiencies, I'd love to hear more about it in what vendors we could take advantage of that with.
**Lucas Felak** (4:35): Yeah, absolutely. So Josh, I think the question is, and I apologize for putting you on the spot here, really one of the things that I think I'd love to know and understand is based on your experience and in the clients that you're supporting, if an account is using CrunchTime, does what Paul and John were told in the implementation process still hold true? And if so, why does it not make sense to have some of the EDI connections with the vendors for the accounting-only module?
**Josh (R365)** (5:15): Gotcha. Yeah. So to be completely honest, I don't have any other clients that use CrunchTime. And I don't know exactly what was explained, Paul, to you in implementation, but I don't understand what would be a negative ramification of having EDI set up from your vendors to your database. Especially, CrunchTime is basically just pulling from Restaurant 365, right.
**Paul Hurley** (5:47): No, no. CrunchTime pulling from our 365? No, no. So, yeah, we're doing it.
**Josh (R365)** (5:55): Yeah. Or are you just uploading or importing stuff from CrunchTime into R365? OK.
**Paul Hurley** (6:01): So the distribution vendors will push the electronic invoices into CrunchTime, right? The second way, right? And then they'll also send us physical invoice copies, right? And then the Quattro team is taking the physical invoice copies.
**Josh (R365)** (6:11): Mm-hmm.
**Paul Hurley** (6:14): They're coding everything to inventory, right? And then we do a reclass at the end of the month, some things go to supplies, and then we do our cost of goods calc, which basically comes right out of...
**Josh (R365)** (6:16): Yeah.
**Paul Hurley** (6:24): CrunchTime. And then they look for any discrepancies, right?
**Josh (R365)** (6:25): Mm-hmm.
**Paul Hurley** (6:29): Because that's the part about it that I like, is that check, right?
**Lucas Felak** (6:31): Right.
**Paul Hurley** (6:32): Is that if there's something missing from CrunchTime or something in CrunchTime that we don't have an invoice for, right? And you know, was it an error? What was it? The weighted average cost of our inventory could potentially be wrong, right? So it was originally just set up like it was originally explained to us that if we wanted to get that type of integration with our distribution vendors, we'd have to go with this inventory module again, which they talked us out of just because it would be kind of duplicative and I don't know if there was an extra charge for it.
**Josh (R365)** (6:49): Mm-hmm.
**Lucas Felak** (6:50): Right.
**Paul Hurley** (6:55): Get that type of integration with our distribution vendors, we'd have to go with this inventory module again, which they talked us out of just because it would be duplicative and I don't know if there was an extra charge for it. I think we were gonna pay more for it. So they just kind of talked us out of it again.
**Josh (R365)** (7:10): Mm-hmm.
**Paul Hurley** (7:10): I think it was gonna make us pay more for it. So they just kind of talked us out of it again.
**Lucas Felak** (7:10): Yeah.
**Josh (R365)** (7:17): Gotcha. OK, that makes a lot more sense. I didn't realize that.
**Lucas Felak** (7:17): Yeah.
**Josh (R365)** (7:22): You did not have the inventory module already, but yeah, I mean basically, if you're already doing that stuff in CrunchTime, then having the EDIs flow straight into our 365, all of that management would then be in R365 instead of CrunchTime. So I don't know if that's a process that you would want to change or I guess maybe my question is, what exactly are you trying to change and why? Unless what you are currently doing is not working for you?
**Lucas Felak** (8:00): So I can answer a little bit of that and then Jeff can jump in from our point of view, right? So to piggyback off of how Paul explained it, the only automation that's currently coming in from any of the accounts payable invoices is going into CrunchTime, so there's some automation happening there, but any of the actual invoice uploads and coding that's happening inside of the Restaurant 365 accounting side of it is being done manually by my team over here at Quattro. And I think the idea here is that if we can bring in some of the EDI that exists inside of the integrations on these vendors, it would significantly reduce the amount of time that it takes to get all of the invoices uploaded. It would allow us to create some automation as far as some regular GL coding, and then we would just reconcile what we have inside of Restaurant 365 versus what's inside of CrunchTime for any discrepancies that are there, as well as then continually manually upload the smaller vendors that don't have the connection to it.
**Josh (R365)** (8:32): OK.
**Lucas Felak** (8:54): It would significantly reduce the amount of time that it takes to get all of the invoices uploaded. It would allow us to create some automation as far as some regular GL coding, and then we would just reconcile what we have inside of Restaurant 365 versus what's inside of CrunchTime for any discrepancies that are there, as well as then continually and continuously manually upload the smaller vendors that don't have the connection to it.
**Josh (R365)** (9:10): Mm-hmm.
**Lucas Felak** (9:10): GL coding, and then we would just reconcile what we have inside of Restaurant 365 versus what's inside of CrunchTime for any discrepancies that are there, as well as then continually manually upload the smaller vendors that don't have the connection to it.
**Paul Hurley** (9:30): Yeah.
**Lucas Felak** (9:30): So it's a half measure because of where it is, but because the larger vendors do have EDI integrations.
**Josh (R365)** (9:31): Gotcha.
**Lucas Felak** (9:40): It significantly increases the automation and efficiency of my team moving forward.
**Josh (R365)** (9:47): OK, that's very helpful. Makes a lot of sense. I guess would you then be OK with doing the invoice management within R365? Because let's say the invoices come in via EDI. Let's say there's an issue with a unit of measurement or a price for a specific vendor item. You said before you were currently doing that within CrunchTime, but if the invoices are coming via EDI straight into our 365, that's technically where the management and upkeep would take place. Is that fine with you and your team to do that within our 365 instead of CrunchTime?
**Lucas Felak** (10:31): Well, follow-up question for you then, right? Because this isn't an either-or situation, right? We don't have to end the current situation as it's being done inside of CrunchTime. It would just allow us to have the information then also flow into Restaurant 365, where we could then manage it there as well.
**Josh (R365)** (10:36): Correct, correct.
**Paul Hurley** (10:51): Yeah, and let me just add to that.
**Josh (R365)** (10:51): Yeah.
**Paul Hurley** (10:52): We cannot end the way that we're doing anything with CrunchTime because it's just a franchise agreement, right?
**Josh (R365)** (10:52): Correct, yeah.
**Lucas Felak** (10:59): Right.
**Paul Hurley** (11:00): Like we have to use that system. That's one of the ways they keep checks and balances with us and everything like that. So we cannot alter or stop doing anything in that system.
**Josh (R365)** (11:10): Yep.
**Paul Hurley** (11:11): So just to be clear.
**Josh (R365)** (11:12): That makes sense and I just wanted to make sure that this also makes sense for you all because...
**Lucas Felak** (11:13): Right.
**Josh (R365)** (11:20): You do only have the accounting module, and in order to get access to inventory and invoices and all of that management, you would need either the inventory or OPS module in order to do so.
**Lucas Felak** (11:34): Yeah, and that's not on the table currently, as Paul explained, for the relationship where the franchise level is. But simply allowing us to bring in the invoices directly so that way we don't have to manually upload that information into the accounting module again would help us speed our deliverables along.
**Josh (R365)** (12:00): Yeah, that makes total sense. And you should. I'm just looking to, I mean, that would essentially be part of accounts payable and accounts receivable, which is part of core accounting, and the EDI point may be separate, but I will have to check up on that with the AE on the account and then get back to you on what that exactly looks like.
**Lucas Felak** (12:12): Yeah.
**Josh (R365)** (12:31): But basically to answer the question, it's totally doable and totally fine to work side by side with CrunchTime if it's all based on automation and efficiency. That's totally possible.
**Paul Hurley** (12:49): Hmm.
**Josh (R365)** (12:49): I just want to make sure that it makes sense for the Quattro brand team if it's going to cost more and you're essentially managing in two different places, making sure that there's a cost benefit there to doing that.
**Lucas Felak** (13:06): Yeah, the way that I see it right now is that we're already managing it in two different places. One of them is just significantly more manual than the other.
**Josh (R365)** (13:10): Fair, fair. Yeah.
**Lucas Felak** (13:16): And any way that we can leverage the technology to give us some of that automation will significantly help us in our AP process, which was ultimately the goal of this call, right? We're trying to really streamline the AP process, and this is a bottleneck for us.
**Josh (R365)** (13:42): Gotcha. I am messaging the AE right now just to give him a heads up and see what we can do in terms of getting you the module necessary for the best price available.
**Paul Hurley** (14:00): So Josh, I guess that's where I'm a little confused. What module do we need just to be able to pull in AP invoices? EDI, I thought you said that was part of core accounting?
**Josh (R365)** (14:11): No. So the AP and AR, the EDI is not. And so I just need AI.
**Lucas Felak** (14:18): So.
**Josh (R365)** (14:20): Just need to figure out if it's just like a one-time EDI setup fee or if that EDI needs to be a part. If that EDI is a part of like an OPS module or inventory module only.
**Lucas Felak** (14:33): So vendor connect is not a part of core accounting.
**Paul Hurley** (14:33): So EDI related to...
**Josh (R365)** (14:40): I was just looking at it and I did not see vendor connect on there, but let me pull it back up real quick. West Bank, GL, APAR, bank rack, document management, budgeting, financial reporting, approval workflows. Oh, vendor connect. OK. Nope, we're good, we're good.
**Lucas Felak** (15:08): Yeah, yeah. OK. That so?
**Josh (R365)** (15:10): We're good.
**Lucas Felak** (15:11): Yeah, I mean this.
**Josh (R365)** (15:13): So then we should be good to go, yeah.
**Lucas Felak** (15:13): Just this, if I remember correctly from my training on all of this, then yeah, this exists inside of it. We're not gonna be able to. There's no inventory management to it. It's simply just pulling in the invoices for the AP and the AR side of it.
**Josh (R365)** (15:24): Yep. Then you should be totally good.
**Lucas Felak** (15:30): Yeah. OK. Yeah, I would be. I was surprised, honestly, when you, like, I, the way I remember it, again, we'll confirm. So all good.
**Josh (R365)** (15:40): Yeah, sorry. When I did that first pass over, I did not see the vendor connect, but it's on there.
**Lucas Felak** (15:43): It's all good. Yeah. Because that would have been new information to me. So yeah, Paul, as far as I understand it, and the way that I've looked at it and again, some of the conversations we've had on our side, too, is that it's really just pulling in the invoice for it right now, and at which point then we can also continue to look at...
**Paul Hurley** (15:58): Yep.
**Lucas Felak** (16:05): The other vendors, Josh, do you feel confident in explaining?
**Paul Hurley** (16:09): Yeah.
**Lucas Felak** (16:14): And what the requirements are to add new EDI vendors. I know that's possible.
**Josh (R365)** (16:25): Yeah. So I dropped an article into the chat basically. Those are all of the vendors that we currently have integrations with right now. If it's not on the list, it doesn't mean it's not possible. It just means we don't have one set up right now, and we can always explore that if need be. I know we for sure have one with Cintas, but basically what happens, and we're kind of already started on one of these, is I send over a vendor template form. You fill that out, send it back to me. I then submit the ticket to our non-POS integrations team, and they go ahead and work with the vendor to set up that direct integration. And then from there, that takes anywhere from about one to three weeks, and then from there, all of the invoices should be flowing over. But it's all done just through our non-POS integrations team. We already have that one ticket set up. They actually reached out to me today and wanted to know if we were still moving forward with it, which I know we put a pause on it until you all talked with Paul and then I guess this call, but that's essentially the crux of it.
**Lucas Felak** (17:31): Yep.
**Josh (R365)** (17:46): We submit the ticket as long as we have the integration available. Our team works with the vendor to set it up.
**Paul Hurley** (17:55): Yeah. So I'm just looking at this list right now, and I see two of our three distributors. I don't see Quantum Distributors, but I also see Tundra Restaurant Supply, right? We get a lot of invoices through Tundra. Let me see. I saw Eagle Lab. I know we use them a little bit, but Cintas, I don't know, did I?
**Lucas Felak** (18:18): They're on here, yeah.
**Paul Hurley** (18:18): I thought they are all right. Yes, would be another one. Yep, I see it.
**John Lavigne** (18:25): Yeah, but Paul, can you hear me?
**Paul Hurley** (18:28): Yep, big credit.
**John Lavigne** (18:30): Cintas. We use the card for.
**Paul Hurley** (18:30): Yeah, we use credit card. Yeah, that's right.
**John Lavigne** (18:34): Yes.
**Paul Hurley** (18:34): But Tundra we do not.
**John Lavigne** (18:36): No, Tundra would be huge for us.
**Paul Hurley** (18:39): Mm-hmm. So yeah, we'd want to definitely pick and choose some and just be smart about this. But yeah, if we can get that, then yeah, just with this, the EDI means that the coding and everything like that, right down to the location level and GL and all that can be programmed in.
**Lucas Felak** (18:44): Course, yeah.
**Paul Hurley** (18:56): So it's gonna kinda happen automatically.
**Josh (R365)** (19:00): Mm-hmm.
**Paul Hurley** (19:01): All right. Yeah, I mean that would be big, right? I mean, that would be a little bit of a later lift for the AP team at Quattro definitely. And then yeah, I mean, it also helps us too, right, John?
**Lucas Felak** (19:11): Right, right.
**Paul Hurley** (19:15): I mean, sometimes invoices get missed, right? And things don't come in. I mean, EDI just has more precision associated with it, so...
**Lucas Felak** (19:26): Yeah, I view this, Paul, as a reallocation of resources on our side away from manual work and back towards reconciliation and checking, which from all of the conversations that I have been in has been...
**Paul Hurley** (19:26): Yeah. Right. It's been a bit of a pain point, right?
**Lucas Felak** (19:48): A consistent ask from you and John that we do more of.
**Paul Hurley** (19:49): Yeah, yeah, yeah.
**Lucas Felak** (19:51): So yes, yeah. So Paul and John, as long as you guys are good with this, I think is Cintas or Tundra or, you know, Kuna. Do we wanna pick one of those to just kinda test it out? And we'll use that as the guinea pig for right now?
**Paul Hurley** (20:15): Regroup. Yeah, I mean I would probably first find out why Quantum's not like what we can do with Quantum Distributors, if we can get that. But yeah, John, let me know if you disagree. I think one of the distributors should be the guinea pig because the coding couldn't be more simple, right? I mean we code everything to inventory and then at the end of the month we run CrunchTime reports, right? Or Rohit does and then gets, you know, cost of goods, supplies, transfers, all that stuff ironed out. But I think it might be a good place to start, like maybe Performance Food Group or something like that, John.
**Lucas Felak** (20:58): Yeah.
**Josh (R365)** (20:58): Well, we have Kuna.
**John Lavigne** (20:59): Yeah, I mean I would.
**Josh (R365)** (21:00): We have Kuna set up.
**John Lavigne** (21:00): I would say Kuna.
**Josh (R365)** (21:01): Yeah, we have that process already started with Kuna. And the tickets have already been submitted, and they're just waiting basically on us for the go-ahead. So if you're comfortable with that, I think that would probably just be the easiest since half of the legwork is already done.
**Paul Hurley** (21:06): Well then, yeah, yeah. I don't think we have an issue with that, I think. OK.
**Lucas Felak** (21:21): Great.
**Paul Hurley** (21:22): Yeah, it didn't matter to me which one we started with, honestly. But I think that makes sense. John, any thoughts?
**John Lavigne** (21:29): Yeah, I mean Kuna goes across multiple states, right? So I think that might be a good one to start with, especially given the volume.
**Lucas Felak** (21:39): Sure. OK. All right. Great deal.
**Paul Hurley** (21:40): Yeah.
**Lucas Felak** (21:43): I'm glad we could all kind of connect on this, Josh. And then also just to get, again, Paul and John are giving go-ahead on that. Josh's main point of contact on our team is gonna be Jeff Morton on this call, and he is on all of the emails as far as communicating with Restaurant 365 directly and then helping to coordinate any conversations with the team. Please keep John and Paul looped in on everything for visibility.
**Josh (R365)** (21:56): OK. Mm-hmm.
**Lucas Felak** (22:09): Side of it, but the vast majority of the deliverables should come from our side.
**Josh (R365)** (22:16): OK, so I will add, I know Paul, you're already on that ticket. And so are you looking this, I'll add Jeff to it as well. Jeff, do you have Restaurant 365 support portal login already? If not, I can set you up with one, because that's basically how the communication will happen.
**Jeff Morton** (22:39): Yes, I have login.
**Josh (R365)** (22:40): Oh, perfect. OK, cool. So then I'll just add you onto that thread, and then any communication from our team will happen within that ticket, and then you could just respond there if need be. And I'm on the ticket as well, so I'll see everything too.
**Lucas Felak** (22:57): OK. Great. Everyone, I appreciate it's a large group, so I appreciate everyone being able to connect at this time and spend a few minutes kind of going over this. I'm excited to see what this looks like, and we'll get this one done once it's complete. Jeff, if you wouldn't mind just let's review it on our side and then we'll connect back with Paul and John and just kind of share any notes back. And then if need be, we'll get back on a call as a group again. I would love to. Those are the types of meetings that I love to cancel when they can just be an email and just say, hey, everything looks good.
**Paul Hurley** (23:37): Yeah.
**Lucas Felak** (23:37): But we'll follow up on all of those things to see. Again, just to highlight what we're seeing on our side, so that way we have visibility, and then we'll hope, hopefully it's something that we find is the future for all of us and then we're just knocking off the rest of them.
**Paul Hurley** (23:54): Sounds good. In the meantime, can we determine if Quantum is gonna be a candidate for this?
**Josh (R365)** (23:55): Awesome.
**Lucas Felak** (24:01): Yeah, we can absolutely do that. And we can talk to Josh about again what establishing a currently unsupported EDI integration looks like, because there is that option. That is also an option that has potential inside of the system. There's a charge to it.
**Josh (R365)** (24:17): Yeah, there are ways to get those files in, even if it's not an EDI. Like we can do...
**Lucas Felak** (24:18): It's a small one-time charge, but it exists.
**Josh (R365)** (24:27): Whether it be like an FTP folder or something like that, but we can. There's definitely ways to get that information in. I will do some research on my side to see if there are any other clients of ours that have something like that with Quantum, and then circle back with you all. And then once the EDI for Kuna is set up, if you have any issues with the integration itself, let's say like a location is not pulling in, but all the rest are, I would respond to the ticket for that. However, if you have any questions for any GL mapping or unit of measurements or coding, that can come straight to me. But if it's an issue with the actual integration, support has to take care of that. But if it's outside of the actual integration, feel free to reach out to me, and I'm happy to hop on a call to talk through any mapping or anything like that.
**Paul Hurley** (25:21): OK. And if any EDI process fails, is it basically the same thing that we have right now with our connection to ServiceChannel? Does it get managed in the same way, Josh?
**Josh (R365)** (25:36): That I do not know. I'm not sure if I'm familiar with your connection with ServiceChannel right now.
**Paul Hurley** (25:42): OK. Yeah, we have like an EDI connection with ServiceChannel where invoices kind of batch and sweep like once a day from FTP coming from ServiceChannel, and if there is no vendor ID, that's the biggest thing that we see. If the vendors don't match in the system, the EDI process breaks and they don't end up importing into 365. I just didn't know what happens if something goes wrong with the management of the EDI process again. Maybe discussion with Quattro as well, like how does that get managed if something breaks? I guess I'm just curious how the process works, or if that's not a typical issue when you're connecting EDI through a vendor. I don't know enough about it, but I know that we do see the process break with our kind of FTP process from ServiceChannel.
**Josh (R365)** (26:39): Gotcha. OK. Yeah. So if there's an issue with the direct EDI vendor to R365, that would just be handled with our non-POS integrations team via support ticket. But usually we don't really see many things breaking. If anything, we see like an invoice not getting uploaded for a specific location on a specific day, and then our team would basically contact, if a support ticket gets submitted.
**Paul Hurley** (26:53): OK. OK.
**Josh (R365)** (27:10): To the non-POS integrations team, our team then talks to the vendor and makes sure that we get that.
**Paul Hurley** (27:17): OK, OK. OK. I just wanted...
**Josh (R365)** (27:26): That file loaded into the system, but yeah, if there's any issues with the EDI, it gets managed through our non-POS integrations team.
**Lucas Felak** (27:26): Yeah.
**Paul Hurley** (27:26): I just wanted to make sure. All right, I don't know what the turnaround time looks like on that if something's broken and we're trying to close.
**Josh (R365)** (27:34): It's pretty quick as long as the information's there. I've seen it where there's been an issue and we can get that resolved pretty quickly, but it also depends on the vendor and their willingness as well. If it's an issue on the vendor end and we're waiting on them, then it's a little bit more difficult. If it's on the R365, then that stuff gets resolved fairly quickly.
**Lucas Felak** (27:58): Yeah, the other thing too, Paul.
**Paul Hurley** (27:59): OK. Right, get the manual.
**Lucas Felak** (28:01): Right. It's just that again the process would be that as long as we would have access to that invoice from CrunchTime or from the way that it's currently being done, our team could bypass whatever the issue is and simply just follow the current standard operating procedure.
**Paul Hurley** (28:22): Yep.
**Lucas Felak** (28:22): As well, so.
**Paul Hurley** (28:24): Yep. And then right, and then make sure that invoice doesn't connect to EDI and then double count, right?
**Lucas Felak** (28:30): Right. Exactly. So truthfully, I think that this offers again, we're just shifting resources away from manual entry and over towards reconciliation.
**Paul Hurley** (28:42): OK.
**Lucas Felak** (28:45): Yeah. OK. All right. Well, thank you, gentlemen, for everyone's time today. Josh, thank you again for joining. We look forward to seeing the information about Kuna getting moving forward, and please if anything comes out again, Jeff will be leading it from our team on a side-by-side. I'll just be involved and make sure that any information gets over to Paul and John if needed.
**Josh (R365)** (29:11): Sounds good. I just reached out to our team to let them know it's approved, so hopefully there should be some communication within that ticket today, and I'm gonna add Jeff to it right now.
**Jeff Morton** (29:22): Thank you.
**Lucas Felak** (29:26): All right. I think that's it. Thanks everyone. Really appreciate your time.
**Josh (R365)** (29:30): Thank you.
**Paul Hurley** (29:31): Thank you.
**Josh (R365)** (29:31): Have a good one.
**Jeff Morton** (29:32): Thank you.