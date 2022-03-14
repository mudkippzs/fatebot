import bs4
from pprint import pprint as pp


def parse_table(soup):
    # Find all the tables in the html.  We'll use this to find the table that contains our data.
    table = soup

    split_table_header = table.find_all('tr')
    header = []
    try:
        header.append(split_table_header[0].contents[1].string)
        header.append(split_table_header[0].contents[3].string)
    except:
        pass

    # The first table is a list of traits and their descriptions.  Skip it.
    rows = soup.find_all('tr')[1:]
    filtered_rows = []
    table_dir = {
        'header': [],
        'rows': []
    }
    counter = 0

    for row in rows:
        row_parsed = []
        for r in row.contents:
            if "\n" not in str(r.string):
                row_parsed.append(str(r.string))
                counter += 1
        filtered_rows.append(row_parsed)

    table_dir["header"] = header
    table_dir["rows"] = filtered_rows

    return table_dir


if __name__ == '__main__':
    test = """
<div id="page-content">
                        

<p><strong>Fast Learner</strong></p>
<p>By buckling down and intently studying certain subjects, the Scion internalizes them in a fraction of the time it would take a lesser intellect. In so doing, he cuts the experience point cost for purchasing dots in Academics, Medicine, Occult, Politics or Science in half, rounding down.</p>
<p><strong>Know–It–All</strong></p>
<p>The Scion is widely read and has a ridiculously well-rounded education. She might not be a master of any single subject, but she knows a little bit about a wide range of disparate, esoteric subjects. (She could explain the intricacies of the Teapot Dome Scandal in terms of the interpersonal dynamics of the Justice League, then explain why typing “while one fork” into a UNIX system is a bad idea, before wrapping up with an explanation of how a Venus’s-ﬂytrap works.) Normally, the burden of portraying this Knack falls to the player, so it behooves her to keep an ear to the ground for obscure trivia she can work into her character’s dialogue during the game. The Storyteller shares a bit of that burden as well, though. During a scene in which the characters seem to be stumped or hopelessly out of options, the Storyteller should “remind” the player of some pertinent bit of obscure trivia her character knows that bears a direct, helpful relevance to the problem at hand. It behooves the Storyteller, then, to make a list of a handful of such helpful hints when he’s designing his story. Just in case.</p>
<p><strong>Math Genius</strong></p>
<p>The Scion is a walking, talking calculator. She can divide up a 10-party restaurant bill so everyone pays only what they owe or calculate the standard deviation of oil prices over the last 15 years, all while holding an intense conversation about whether Republicans or Democrats are worse tippers. As long as she knows all the ﬁgures involved, she can crunch the numbers in her head with only a moment’s pause. She can also use mathematical shorthand and rapid calculation to estimate things like how many jellybeans are in a glass jar at the State Fair or how many titanspawn-possessed Civil War re-enactors are currently rushing toward her across the picnic grounds.</p>
<p><strong>Perfect Memory</strong></p>
<p>The character remembers everything about his past from before the game started to the current moment in the story. If ever the player forgets a salient point or key bit of information from previous sessions, he has but to ask the Storyteller and the Storyteller will remind him. It’s a good idea for the character’s player to take copious notes on each session’s events and double-check them with the Storyteller, if only to alleviate some of the stress on the Storyteller.</p>
<p><strong>Teaching Prodigy</strong></p>
<p>With this Knack, a Scion can help someone else become a fast learner (per the eponymous Knack). When she makes signiﬁcant efforts to tutor a student in a subject—a distinction best left up to the Storyteller—the experience point cost for purchasing dots in the Ability the teacher teaches is cut in half, rounded down. The catch built into this Knack is that a Scion cannot teach a student an Ability that she (the teacher) doesn’t have. Nor can the teacher help a student surpass her in mastery of a subject—which is to say, the Scion cannot teach her student more dots in an Ability than she (the teacher) has.</p>
<p><strong>Cipher</strong></p>
<p>The Scion’s brain is his own personal Enigma machine. He can break any encryption and decode any message created by someone without Epic Intelligence, without the need for a roll. He can also design a one- time code for a speciﬁc recipient that cannot be broken by anyone without Epic Intelligence (regardless of how smart such a person is or what decryption equipment he might have on hand). Only a fellow Scion with Epic Intelligence can even attempt to break the code—calling for opposed (Intelligence + Academics) rolls. The person for whom the coded message is intended can automatically read the message as clearly as if it were written in his native language.</p>
<p><strong>Language Mastery</strong></p>
<p>The Scion can understand any language that is spoken to him. Once he’s heard a few sentences, he can then speak that language back as if he grew up among native speakers. Writing the language is a bit trickier, as he can only transliterate his written words in the alphabet of his native language until someone teaches him the alphabet and punctuation of the new language. For instance, say a Scion with this Knack whose native language is English has picked up French at Orly Airport in Paris and would like to leave a thank-you note for a bartender who gave him helpful information. That Scion might write, “Mare- see du mah-vay zayday,” to express his thanks, when what he really means is, “Merci de m’avez aidé.” Likewise, reading the new language can be difﬁcult if that language uses characters that don’t appear in an alphabet with which he is already familiar.</p>
<p><strong>Multitasking</strong></p>
<p>The Scion can carry on as many separate primarily mental activities as he has dots of Legend simultaneously and with his full attention. A Scion with Legend 6 could play a game of chess against a recognized master while also playing go against a ninth-dan professional, translating a James Joyce novel into a different language, reprogramming his computer, planning a raid against the titanspawn entrenched in the historic ruins across town and itemizing his various businesses’ tax deductions for the year. The character never suffers distraction penalties for mental actions, nor are his separate simultaneous mental actions penalized as per the multiple action rules (see Scion: Hero, p. 179).</p>
<p><strong>Star Pupil</strong></p>
<p>Prerequisite Knack: Fast Learner (Scion: Hero, p. 135) The Scion is now a better student than ever before. Not only does he learn the prerequisite Knack’s listed subjects far more rapidly than normal, he now learns Athletics, Brawl, Craft, Control, Investigation, Larceny, Marksmanship, Melee, Survival and Thrown at the reduced experience point cost. Having a Scion teacher with the Teaching Prodigy Knack doubles the reduction again, just as it does for the prerequisite Knack.</p>
<p><strong>Wireless Interface</strong></p>
<p>If the Scion devotes his total attention to doing so, he can mentally interface with an active computer without so much as touching it. He need only be able to see the computer, though not necessarily the monitor, in order to communicate with it. (Also, the computer must be turned on. Anybody can talk to a computer that isn’t on. Same thing happens too.) The degree to which the Scion can program the computer or access its ﬁles is the same whether he’s sitting at a keyboard in front of a monitor or just staring at its CPU, though, so it behooves him to at least know his way around an interface. Mentally interfacing with a computer’s programming absorbs the Scion’s attention, imposing a -2 distraction penalty on him unless he also has the Multitasking Knack.</p>
<p><strong>Blockade of Reason</strong></p>
<p>Charmers and hucksters and blowhards can get their way with even the Gods themselves, as the Gods can be tricked and led astray almost as easily as mortals can. Characters with Epic Intelligence and this Knack, however, can block out even the most charming words with a simple application of reason. When some other character uses a supernatural persuasion effort—including the addition of bonus dice from an Epic Attribute—that calls for a mental resistance roll of (Willpower + Integrity + Legend), the character with this Knack can apply her bonus successes from her Epic Intelligence to that roll. Doing so costs her one Legend point per resistance roll.</p>
<p><strong>Instant Translation</strong></p>
<p>Prerequisite Knack: Language Mastery (Scion: Demigod, p. 65) As regards the spoken word, this Knack provides much the same benefit as its prerequisite. Yet where Language Mastery requires that the character listen for a while to get a sense of the strange language’s ebb and flow, this Knack allows the character to understand anything that is said to him in any language the moment it is spoken. Where this Knack truly surpasses its prerequisite is that it allows the character to read any written language with which he isn’t familiar, even if it’s written in characters that are completely alien to him. He can’t automatically write with perfect fluency in a new language he can speak or has read, but his written vocabulary is as broad as every word in that language that he has read.</p>
<p><strong>Speed Reader</strong></p>
<p>The character can read and comprehend with perfect clarity an entire block of text—such as two facing pages of an open book—in the amount of time it takes her to blink. She need only be able to see the entire block clearly enough to focus her eyes on any given word in it.</p>
<p><strong>Telepathy</strong></p>
<p>The character’s mind is so powerful that he can think thoughts directly into other people’s brains for them. These thoughts come through in a recipient’s head as words spoken in the sender’s voice, and are recognizable as coming in from outside. The sender must be able to see the person whom he intends to address thus, and he must spend one Legend point per sent thought (i.e., per sentence). If the sender has the Multitasking Knack (from Scion: Demigod, p. 65), he can send the same thought to several people at once. The sender cannot receive telepathic information from a recipient unless the recipient also has Telepathy and spends the Legend point to use it.</p>
<p><strong>Well-Read Virgin</strong></p>
<p>Prerequisite Knack: Know-It-All (Scion: Hero, p. 135) The character has such a wealth of knowledge that even if she has never performed a particular activity, she can still discuss it or research it like an expert. As such, the player can apply the character’s Epic Intelligence bonus dice to any Intelligence-based roll required to glean information, regardless of whether the character has any dots in the Ability in question. For instance, identifying what martial arts style someone is using would require an (Intelligence + Brawl) roll. With this Knack, a character with no dots in Brawl could handily identify the style, the particular variant of it the student is using and who the student’s teacher most likely was. This Knack works only for rolls intended to dredge up information.</p>
<p><strong>Fight With Your Head</strong></p>
<p>A Scion with this Knack possesses a truly superhuman sense of strategy. He anticipates an enemy’s evasions, counter-strategies and gambits with ease. He can reason around a berserker’s shock and awe or calculate a dodging foe’s final location to slip past that foe’s defenses. He can find just the right angle to slip from an opponent’s grasp, and he can see through feints and other ploys with ease. The Scion activates this Knack by selecting an opponent and spending one point of Legend. For the rest of the scene, he counteracts the automatic successes, bonus dice and similar benefits conferred by other Knacks and Boons. The total number of such bonuses counteracted cannot exceed the Scion’s automatic success from Epic Intelligence. This Knack can negate bonuses from Knacks and Boons, as well as automatic successes and bonuses from Epic Attributes themselves. It does not affect stunt bonuses or extra dice from invoking Virtues. If an opponent receives more bonuses than a Scion can counteract, the user of this Knack picks what he will negate. This Knack might seem an odd one to include in a book about the Norse and their Gods. In truth, despite their famed fury and aggression, Norse warriors valued a cunning fighter at least as much as a frenzied powerhouse.</p>
<p><strong>Axiom</strong></p>
<p>After running into ambushes featuring no less than two dozen animated sand-golems with stone hearts, a Scion begins to wonder if there’s some sort of pattern behind the attacks. The logical mind of a Scion with Epic Intelligence puts those patterns together and determines some viable conclusion. Once the sand-golems have been defeated, for instance, the Scion might theorize that since they are all made from sand, their creator must reside somewhere with a surfeit of sand — some desert. Normal people create theories like this all the time, but Scions with this Knack create theories that are correct. The Scion’s player spends three points of Legend and rolls (Intelligence + appropriate Ability + Legend). The Ability used will depend upon the axiom in question: Deriving a scientific fact about something uses Science, while relying on observed clues to deduce a suspect uses Investigation. The Scion must then state the axiom clearly, such as “I deduce from the presence of so much sand in these golems that the creator must reside within a desert,” or “The constant attacks by ninja imply that our enemy must be related somehow to the Amatsukami.” If the player’s roll succeeds, the Storyteller will respond with “true,” meaning that the Scion’s claim is known to be true; “false,” meaning that the claim is known to be false; or “incorrect,” meaning that the Scion has proceeded from a false assumption (perhaps forgetting that the ambushing ninja were all clones of Jean-Claude van Damme). If the Storyteller had already planned out that element of the adventure, then the player learns what the Storyteller had in mind by virtue of the power; if the Storyteller had left the element undecided, then his answer to the player’s Axiom essentially enforces how that part of the story will unfold. The Scion logically knows exactly what to expect, and she knows immediately if her best guess is right, wrong, or founded on a mistake that she made. The difficulty of the roll depends upon the scope of the statement. Nailing down a simple fact, such as “All of these attackers use cheap guns, so their boss must be poor,” has a low difficulty (1-5). Nailing down a more wide-ranging fact, such as “Despite their varied forms, all of these titanspawn are all susceptible to silver, so we should prepare to use the powers of the Moon against them,” has a moderate difficulty (6-15). Facts that affect the Overworld or Underworld, or that nail down specifics with exacting detail, are severely difficult (25+). The difference between a normal deduction and a fact nailed down with Axiom is that the Scion’s stated fact (if confirmed by the Storyteller) is known to be right. Essentially, the Scion’s player states something that will be true or will be false about the rest of the story. The Scion can use this Knack only once per scene.</p>
<p><strong>Concept To Execution</strong></p>
<p>Prerequisite Knacks: Fast Learner (Scion: Hero, p. 135), Star Pupil (Scion: Demigod, p. 65) Ancient Gods with a particular joy for creation, such as Ptah and Hephaestus, often delight in unleashing strange scientific devices on an unsuspecting populace (or Scion). Scions who turn their prodigious intellect to the construction of curiosities often try to find ways to make useful tools, entertaining toys or devious traps. All three are possible for the mind capable of taking an idea from concept to execution. With Epic Intelligence and the Craft and Science Abilities, a Scion can manufacture a wide range of items, but this Knack enables the Scion to build uncanny devices that defy conventional reason or function. Gadgets created by Scions have three primary possible functions:</p>
<ul>
<li>Replace another item’s function: For instance, creating a quick repair for a broken carburetor, using an aluminum can and a bicycle tube. Such a fix can temporarily restore function to a “mundane” (non-magical) item, such as a car, a computer or an orbital shuttle.</li>
<li>Temporarily replace a Relic: The Scion can use his innate knowledge of design and creation to make an object that can substitute for a missing or damaged Relic. The replacement allows its wielder to access one Purview that the original missing or damaged Relic normally provided. Replacement Relics require the creating Scion to imbue the item with a bit of ichor as power, which means suffering a level of lethal damage (with no soak) in order to bleed out some ichor to fuel the item.</li>
<li>Perform a specialized new function: The Scion creates a device with functions not found among the more “common” tools of the World. The Golden Servant of Hephaestus (Scion: Demigod, pp. 228-229) would be an example of this.</li>
</ul>
<p>As a general principle, items that replace another item’s function or temporarily replace a Relic are temporary. The Scion’s player spends five points of Legend and rolls (Intelligence + Craft + Legend). The difficulty depends upon the object, as shown in the accompanying table. This is an extended task of the Miscellaneous type, so it can be done in the midst of combat as the Scion theorizes, tears apart available materials and comes up with a solution on the fly. The temporary component functions for one use or (if the crafting Scion’s player spends a point of Willpower) for the rest of the scene.<br></p>
<table class="wiki-content-table">
<tbody><tr>
<td>Size</td>
<td>Modifier</td>
</tr>
<tr>
<td>Item is larger than a breadbox or smaller than a car key</td>
<td>+3</td>
</tr>
<tr>
<td>Item is larger than a person or smaller than a thumbtack</td>
<td>+5</td>
</tr>
<tr>
<td>Item is larger than a car or smaller than a grain of rice</td>
<td>+10</td>
</tr>
<tr>
<td>Item is larger than a battleship or microscopic</td>
<td>+15</td>
</tr>
<tr>
<td>Complexity</td>
<td>Modifier</td>
</tr>
<tr>
<td>Item has many moving parts</td>
<td>+3</td>
</tr>
<tr>
<td>Item has many intricate moving parts</td>
<td>+5</td>
</tr>
<tr>
<td>Item uses electricity</td>
<td>+10</td>
</tr>
<tr>
<td>Item uses micro-circuitry</td>
<td>+15</td>
</tr>
<tr>
<td>Dramatic Relation</td>
<td>Modifier</td>
</tr>
<tr>
<td>Item has only a peripheral relation to the story</td>
<td>+3</td>
</tr>
<tr>
<td>Item has no relation to the story</td>
<td>+5</td>
</tr>
<tr>
<td>Item runs counter to part of story, theme or plot</td>
<td>+10</td>
</tr>
</tbody></table>
<p>Specialized new items rely on the Scion exploiting (or writing) new scientific principles. Creation of such devices can take months or years of time; the extended test uses (Intelligence + Science + Legend) to theorize the item, then (Intelligence + Craft + Legend) to build it. The difficulty for such a task typically begins at 35 and can increase due to object size and complexity (as well as how relevant it is to the story at hand; see the sidebar for some suggestions). If the item performs some otherwise impossible task or would radically change day-to-day life for the common man — cheap, clean fusion power, flying cars starting at $100, an algorithm that proves that P = NP — the base difficulty ranges from 50 to 100, and the task can only be completed by a God. Thanks to the interference of Fate, any object that would completely hamstring a dramatic moment or reshape the cosmic order is simply beyond the magnitude of capabilities for even a God with this Knack. Also, the Scion must have some sort of tools or materials to work with. Trapped in the Mojave, the Scion can’t make a moisture condenser out of sand, but in a junkyard, the Scion could construct a miniature tank.</p>
<p>Caveat: Based on pantheon and character concept, additional options may be available than purely technological devices</p>
<p><strong>Tactical Planning</strong></p>
<p>Usually, personal combat relies heavily on quick thinking and razor-sharp timing. A Scion with the Tactical Planning Knack, though, thinks three moves ahead of everyone else on the battlefield. With her excellent command of the battle situation and her prepared contingency plans, she’s able to react by using a previously-developed script instead of falling back on reflexes. As long as she isn’t surprised, the Scion can choose to substitute her Intelligence score (including Epic Intelligence) for her Wits when making Join Battle rolls.</p>

                    </div>
"""
    pp(parse_table(test))
