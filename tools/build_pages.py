"""Builds content/*.html (block markup) for the inner pages. Run: python3 tools/build_pages.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from blocks import *

OUT = os.path.join(os.path.dirname(__file__), '..', 'content')

def feature(img, alt, inner, flip=False, bg=None, text=None, anchor=None):
    pic = column(image(img, alt), 'center')
    txt = column(inner, 'center')
    return section(columns([txt, pic] if flip else [pic, txt]), bg=bg, text=text, anchor=anchor)

def write(name, parts):
    open(os.path.join(OUT, name), 'w').write("\n\n".join(parts) + "\n")

# ---------------- About (page 159) ----------------
def about():
    t = []
    t.append(page_hero('Who we are', 'the voice of Hamilton’s African Diaspora Community at the municipal, provincial and federal levels'))
    t.append(section(
        para('Hamilton Black Health Community Leaders Forum is the voice of Hamilton’s African Diaspora Community at the municipal, provincial and federal levels. The organization represents Hamilton’s African Communities before the city of Hamilton, and the provincial and federal governments in the spirit of partnership for the advancement of its member-unique needs regarding the social determinants of health. HBHCLF, a federally registered, non-partisan and non-profit organization was established on September 14, 2021. and will be inaugurated on May 28th, 2022', 'large')
        + "\n\n" + para('We are governed by a constitution and specific bylaws agreed to by our membership and represent the interest of Canadians of African heritage residing in Hamilton at the Municipal, Provincial and Federal levels on policy-oriented issues that impact them in areas such as housing, access to equitable and culturally-delivered healthcare, employment, and other social determinants of health.'),
        content='900px'))
    mission = heading('Our mission', 2, 'x-large') + "\n\n" + para('We seek inclusive health policy-making at all levels of government, advocating for equitable and culturally appropriate healthcare, housing, and employment opportunities for our community.') \
        + "\n\n" + heading('Aims', 2, 'x-large') + "\n\n" + para('Our aim is to foster a strong, unified voice that promotes and advocates for the health and well-being of the African Diaspora in Hamilton.')
    t.append(feature(U + '2024/08/About-Us-1.jpg', '', mission, bg='orange', text='black'))
    goals = [
        ('Partnerships', '2024/08/Partnerships-1.jpg', [
            'Seek to form partnerships with organizations to engage in Projects aimed at addressing issues related to social determinants of health within the African Diaspora in Hamilton.',
            'Collaborate with organizations to work on existing policies and operations which negatively affect the overall health & well-being of the African Diaspora in Hamilton and request involvement in policy reviews, discussions and enactment to effect systemic changes.',
            'Collaborate with other Black Organizations on Projects of mutual interest to achieve equity, diversity and inclusion for our communities. We will also share useful ideas, resources, data and information for our mutual benefit.']),
        ('Research & Data Collection', '2024/08/Research-Data-Collection.jpg', [
            'Collect race-based data as a key step to improving health outcomes for African populations and addressing racism.',
            'To build pictures of where race-based gaps, racism and racial bias exist in both Provincial and Municipal health, housing, employment, school, and Justice systems.',
            'To paint a picture of the gaps and barriers in services and programs for African children, youth and families to effect changes to support their mental health and wellbeing.',
            'To share data collected with local and provincial governments, public organizations, and agencies to make culturally effective interventions and policy changes.',
            'To improve government funding allocations to Racialized and marginalized communities such as ours.']),
        ('Community Engagement', '2024/08/Community-Engagement.jpg', [
            'Public Education through Town Hall meetings and Forums', 'Awareness Campaigns', 'Conferences', 'Presentations to both Public & Private Agencies']),
    ]
    cols = [column(image(U + p, '') + "\n\n" + heading(h, 3, 'large') + "\n\n" + lst(items), 'top') for h, p, items in goals]
    t.append(section(heading('Our goals', 2, 'x-large', 'center') + "\n\n" + columns(cols, 'top')))
    t.append(feature(U + '2024/08/Vaccine-Ambassado.jpg', '',
        heading('Hamilton Vaccine Ambassador Program', 2, 'x-large')
        + "\n\n" + para('Hamilton Black Health Community Leaders Forum’s aims to become the unified voice of the African Diaspora communities in Hamilton on issues related to social determinants of health.')
        + "\n\n" + para('During the COVID pandemic, our communities came face to face with its devastating effects on our members.')
        + "\n\n" + para('Majority of our people in Hamilton live in multigenerational homes and most families found it very difficult to quarantine while living in an apartment.')
        + "\n\n" + button('Learn more', '/programs/#Vaccine_Ambassadors')))
    t.append(feature(U + '2024/08/Seniors-Hangout.jpg', '',
        heading('New Horizon Seniors Project', 2, 'x-large')
        + "\n\n" + para('Hamilton Black Health Community Leaders Forum’s aims to become the unified voice of the African Diaspora communities in Hamilton on issues related to social determinants of health.')
        + "\n\n" + button('Learn more', '/programs/#New_Horizon'), flip=True))
    def people(rows):
        return "\n\n".join(heading(n, 3, 'medium') + "\n\n" + para(r) for n, r in rows)
    exe = [('Ikechukwu Agbassi', 'President'), ('Jean-jacques Somwe', 'Vice President'), ('John Luma', 'Financial Director'), ('Comfort Afari', 'Interim Administrative Assistant'), ('Salma Ahmed Musa', 'Executive Assistant')]
    brd = [('Comfort Afari', 'Board Chairman'), ('Matilda Ansah-Sam', 'Board Member, Treasurer/Director Finance, Audit & Risk'), ('Nancy Muinda', 'Board Member, Director Program Planning & Implementation'), ('Chuma Okereke', 'Board Member, Director, Nomination, Recruitment & Partnership'), ('Innocent Azipoh', 'Board Member, Service Excellence/Equity & Diversity')]
    t.append(section(columns([column(heading('The executive team', 2, 'x-large') + "\n\n" + people(exe), 'top'), column(heading('The governing board', 2, 'x-large') + "\n\n" + people(brd), 'top')], 'top'), bg='black', text='white', anchor='team'))
    write('about.html', t)

# ---------------- Programs (page 177) ----------------
def programs():
    t = [page_hero('Our programs', 'to unite people of African heritage living in Hamilton')]
    t.append(feature(U + '2024/08/Africa-Day.jpg', '', heading('Africa Day', 2, 'x-large') + "\n\n" + para('The Africa Day celebration in Hamilton, Ontario, is a vibrant annual event that unites the city’s African community and its supporters around May 25th, honoring African heritage and culture. This gathering features a rich array of activities, including cultural showcases of arts and crafts, thought-provoking lectures by community leaders, lively music and dance performances, and a culinary experience featuring authentic African cuisine. Organized by the Hamilton Black Health Community Leaders Forum, the celebration fosters unity among people of African descent, promotes cross-cultural understanding, empowers youth, and highlights the contributions of the African community to Hamilton’s diverse cultural landscape.')))
    t.append(feature(U + '2026/09/Inahita-Kijiji-Kulea-Mtoto-–-African-Children.png', 'Smiling Black African children gathered together, representing community, care, and belonging.',
        kicker('Featured program') + "\n\n" + heading('Inahitaji Kijiji Kulea Mtoto', 2, 'x-large') + "\n\n" + heading('It Takes a Village to Raise a Child', 3, 'large')
        + "\n\n" + para('A culturally responsive, community-led support program for Black/African and newcomer families in Hamilton who are navigating or engaged with the child-welfare system.')
        + "\n\n" + button('Learn more', '/inahita-kijiji-kulea-mtoto/'), flip=True, bg='orange', text='black'))
    t.append(feature(U + '2026/07/HBHCLF-Ubuntu.jpg', '',
        heading('Ubuntu Seniors Program', 2, 'x-large')
        + "\n\n" + para('The Ubuntu Seniors Program is an initiative of the Hamilton Black Health Community Leaders Forum created to celebrate, support, and engage seniors through meaningful social, recreational, and wellness-focused activities.')
        + "\n\n" + para('Sponsored by the Hamilton Community Foundation Martin Fund Grant and the Hamilton Urban Core Community Health Center, in partnership with NURU Hamilton, the program provides safe and joyful opportunities for seniors to connect, stay active, build friendships, and feel valued within the community.')
        + "\n\n" + para('From interactive gatherings to bowling at Splitsville Hamilton and the Seniors Tour of Niagara Falls, the Ubuntu Seniors Program reflects the spirit of community care, inclusion, dignity, and togetherness.')
        + "\n\n" + buttons([('Seniors Bowling @ Splitsville Hamilton', '/seniors-bowling-splitsville-hamilton/'), ('Seniors Tour of Niagara Falls', '/seniors-tour-of-niagara-falls/')])))
    t.append(feature(U + '2024/09/MentorAction.jpg', '',
        heading('MentorAction', 2, 'x-large')
        + "\n\n" + para('The Hamilton Black Health Community Leaders Forum is proud to partner with Interval House of Hamilton in their MentorAction program. This collaboration is dedicated to addressing gender-based violence within our community by providing specialized training to community members.')
        + "\n\n" + para('MentorAction is a program that empowers men to take an active role in ending gender-based violence. Through education, mentorship, and community involvement, the program challenges harmful societal norms and promotes a culture of respect and safety. By partnering with MentorAction, we aim to ensure that the African community in Hamilton is equipped with the knowledge and tools needed to recognize, prevent, and stand up against gender-based violence.')
        + "\n\n" + para('As part of this initiative, community members will receive comprehensive training on how to address and intervene in situations of gender-based violence, fostering a supportive and informed network within our community. Together, we are committed to creating a safer, violence-free environment for all.'), flip=True, bg='black', text='white'))
    t.append(feature(U + '2024/08/Seniors-Hangout.jpg', '',
        heading('New Horizon Seniors Project', 2, 'x-large')
        + "\n\n" + para('The New Horizon Seniors Project, funded by the Canadian Government, is an initiative by the Hamilton Black Health Community Leaders Forum aimed at enhancing the well-being of seniors in our community. This program fosters social interaction and engagement among seniors, addressing the mental, physical, and psychological challenges they face. Through a variety of activities and support networks, the project seeks to alleviate isolation, promote health, and ensure that our seniors lead fulfilling lives within a supportive community.'), anchor='New_Horizon'))
    t.append(feature(U + '2024/09/VAW.jpg', '',
        heading('Violence Against Women (VAW)', 2, 'x-large')
        + "\n\n" + para('Since 2021, the Black Health Community Leaders Forum and Interval House of Hamilton have come together in a groundbreaking collaboration to better serve the African community in Hamilton. Together, they have established a dedicated position for an African Outreach Worker, specifically focused on providing Violence Against Women (VAW) support within the community. This initiative reflects their shared commitment to addressing the unique challenges faced by African women and ensuring they have access to the culturally sensitive resources and support they need. Through this partnership, they are making strides in creating a safer and more supportive environment for African women in Hamilton.'), flip=True, bg='green', text='black'))
    vac = [
        'The Hamilton Black Health Community Leaders Forum (HBHCLF) is dedicated to becoming the unified voice for the African Diaspora communities in Hamilton, particularly regarding issues tied to the social determinants of health. The COVID-19 pandemic starkly highlighted the vulnerabilities within our community, exposing significant challenges that our members faced.',
        'Many individuals in our community live in multigenerational households, often within confined apartment spaces, making self-isolation and quarantine efforts nearly impossible. Communication barriers further compounded these difficulties, particularly in accessing essential primary health care services. This lack of access, coupled with the stress of social isolation, anti-Black racism, and the mental health struggles many of our community members experience, led to increased anxiety, depression, and in some cases, suicidal thoughts.',
        'A particularly pressing issue during the pandemic was the high level of vaccine hesitancy within our community. Deep-seated distrust in the public health system, fueled by historical injustices like the Tuskegee experiment, led to widespread fear and skepticism about the rapid development and safety of the COVID-19 vaccines. This lack of trust was exacerbated by the absence of African representation in decision-making bodies, leaving our community feeling marginalized and overlooked.',
        'In response to these challenges, the HBHCLF partnered with Hamilton Urban Core Health Centre and Hamilton Public Health to address vaccine hesitancy among African, marginalized, and racialized communities in Hamilton. We proposed the Vaccine Ambassador Program, which was designed to build vaccine confidence through the efforts of trusted individuals within the community. These Vaccine Ambassadors were tasked with educating their peers about vaccine safety and efficacy, sharing personal experiences, and addressing concerns directly.',
        'The program, enthusiastically supported by Hamilton Public Health, was successfully launched with the following primary goals:']
    goals = [('Building Confidence', ['Promote community support for COVID-19 vaccination.', 'Distribute reliable information and resources about vaccines.', 'Act as a bridge between community members and necessary support services.']),
             ('Building Trust', ['Partner with community leaders, organizations, and networks.', 'Provide guidance, support, and interpretation at vaccine clinics.', 'Offer accessible, informed answers to vaccine-related questions.']),
             ('Sharing Information', ['Disseminate vaccine, health, and support information within the community.', 'Communicate community experiences to Hamilton Public Health.', 'Help shape Hamilton’s vaccine response based on community feedback.'])]
    tail = ['On May 17, 2021, nine Vaccine Ambassadors were hired to launch this program, with additional ambassadors joining shortly after. Today, the team consists of 11 members who are deeply connected to various communities in Hamilton. They bring a diverse range of linguistic skills, speaking languages including Arabic, French, Nuer, Dazaga, Vietnamese, Mandarin, Spanish, Hindi, Rajasthani, Gujarati, and Punjabi.',
            'The Vaccine Ambassadors have been thoroughly trained to engage with communities across the city and work closely with Hamilton Public Health’s Vaccine Confidence Team to stay informed and up-to-date. They also collaborate with the Vaccine Readiness Network to enhance their outreach efforts.']
    body = heading('Hamilton Vaccine Ambassador Program', 2, 'x-large') + "\n\n" + "\n\n".join(para(p) for p in vac)
    body += "\n\n" + columns([column(heading(h, 3, 'large') + "\n\n" + lst(i), 'top') for h, i in goals], 'top')
    body += "\n\n" + "\n\n".join(para(p) for p in tail)
    body += "\n\n" + para('The Vaccine Ambassadors continue their mission to reach racialized and marginalized communities in Hamilton. If you are interested in collaborating with a Vaccine Ambassador for a community outreach event, please contact <a href="mailto:vaccineambassador@hamilton.ca">vaccineambassador@hamilton.ca</a>.', raw=True)
    body += "\n\n" + para('For more information on building COVID-19 vaccine confidence, visit the <a href="https://www.hamilton.ca/coronavirus/covid-19-vaccine-resources">City of Hamilton’s COVID-19 Vaccine Resource</a>.', raw=True)
    t.append(section(body, content='900px', anchor='Vaccine_Ambassadors'))
    write('programs.html', t)

# ---------------- Gallery (page 722) ----------------
def gallery():
    items = [
        ('Seniors Tour of Niagara Falls', 'June 13, 2026', '2026/06/IMG-20260625-WA0036.jpg', 'seniors-tour-of-niagara-falls'),
        ('2026 Africa Day Celebration', 'May 28, 2026', '2026/05/MACM3651-scaled.jpg', '2026-africa-day-celebration'),
        ('Seniors bowling @ Splitsville Hamilton', 'April 26, 2026', '2026/04/WhatsApp-Image-May-6-2026-3.jpeg', 'seniors-bowling-splitsville-hamilton'),
        ('2025 Africa Day Celebration', 'May 24, 2025', '2025/05/DSC_5003.jpg', '2025-africa-day-celebration'),
        ('2025 Africa Day Symposium', 'May 17, 2025', '2025/05/CT2A1795-scaled.jpg', '2025-africa-day-symposium'),
        ('African Leaders Breakfast Meeting', 'January 18, 2025', '2025/01/ALBM-2025-01-18-at-20.28.09.jpeg', 'african-leaders-breakfast-meeting'),
        ('2024 New Horizon Seniors Day', 'July 14, 2024', '2024/08/IMG-20240714-WA0064.jpg', 'africa-day-2024-2'),
        ('2024 Africa Day Celebration', 'May 25, 2024', '2024/08/Africa-Day.jpg', 'africa-day-2024'),
        ('2023 Africa Day Celebration', 'May 27, 2023', '2024/08/2023_05_27_9999_172Bryan_80th.jpg', 'africa-day-2023'),
        ('2022 Africa Day Celebration', 'May 28, 2022', '2025/06/Main.png', '2022-africa-day-celebration'),
    ]
    def card(title, date, img, slug):
        link = f'/{slug}/'
        return column(
            f'<!-- wp:image {{"sizeSlug":"large","linkDestination":"custom","style":{{"border":{{"radius":"12px"}}}}}} -->\n<figure class="wp-block-image size-large has-custom-border"><a href="{link}"><img src="{U}{img}" alt="{title}" style="border-radius:12px"/></a></figure>\n<!-- /wp:image -->'
            + "\n\n" + para(date, 'small') + "\n\n" + f'<!-- wp:heading {{"level":3,"fontSize":"medium"}} -->\n<h3 class="wp-block-heading has-medium-font-size"><a href="{link}">{e(title)}</a></h3>\n<!-- /wp:heading -->', 'top')
    rows = []
    for i in range(0, len(items), 3):
        c = [card(*x) for x in items[i:i + 3]]
        while len(c) < 3: c.append(column('', 'top'))
        rows.append(columns(c, 'top'))
    write('gallery.html', [page_hero('Media Gallery', 'Yes! We love taking photos'), section("\n\n".join(rows))])

# ---------------- Contact (page 216) ----------------
def contact():
    form = heading('Send a quick message', 4, 'large') + "\n\n" + para('[Contact form goes here. It is built with Fluent Forms in phase 6, with fields Full Name, Phone, Email and Message, sending to info@hbhclf.org.]', 'small')
    details = (heading('Want to meet in person?', 4, 'large') + "\n\n" + heading('Coffee is on us', 2, 'x-large')
        + "\n\n" + heading('Give us a call', 3, 'medium') + "\n\n" + para('289-408-8634')
        + "\n\n" + heading('Our mailing address', 3, 'medium') + "\n\n" + para('268-762 Upper James Street, Hamilton, ON L9C3A2')
        + "\n\n" + heading('Shoot us an email', 3, 'medium') + "\n\n" + para('<a href="mailto:info@hbhclf.org">info@hbhclf.org</a>', raw=True))
    t = [page_hero('Contact us', 'We would be happy to assist you'),
         section(columns([column(form, 'top'), column(details, 'top')], 'top')),
         section(html_block('<iframe title="Map of Hamilton, Ontario" src="https://maps.google.com/maps?q=Hamilton%2C%20Ontario&amp;t=m&amp;z=10&amp;output=embed&amp;iwloc=near" width="100%" height="380" style="border:0;border-radius:16px" loading="lazy"></iframe>'), pad='40')]
    write('contact.html', t)

# ---------------- Newcomers (page 1071) ----------------
def newcomers():
    write('newcomer-questionnaire.html', [page_hero('Newcomer Questionnaire', 'Your response will assist us to better equip ourselves to help.'),
        section(shortcode('[fluentform id="3"]'), content='800px')])

# ---------------- Inahitaji (page 1780) ----------------
def inahitaji():
    t = []
    t.append(section(columns([column(heading('Inahitaji Kijiji Kulea Mtoto', 1, 'hero') + "\n\n" + heading('It Takes a Village to Raise a Child', 2, 'large')
            + "\n\n" + para('A new culturally responsive, community-led support program for Black/African and newcomer families in Hamilton who are navigating or engaged with the child-welfare system.')
            + "\n\n" + para('Stronger families. Connected communities. Children who flourish.', bold=True), 'center'),
        column(image(U + '2026/09/Inahita-Hero-Family-Unity.png', 'Multigenerational Black African family and community worker gathered around smiling children in a warm supportive scene.'), 'center')]), bg='black', text='white', reveal=False))
    t.append(section(heading('Your family is part of a village.', 2, 'x-large') + "\n\n" + para('You do not have to navigate the journey alone. This initiative is designed around listening, cultural understanding, practical connection and family resilience.', 'large') + "\n\n" + para('Your culture matters. Your family matters. Your community matters.', bold=True), content='900px', bg='orange', text='black'))
    t.append(section(heading('You don’t have to navigate it alone', 2, 'x-large') + "\n\n"
        + para('For a family, involvement with the child-welfare system can bring uncertainty, difficult conversations, unfamiliar processes and questions about where to find help.')
        + "\n\n" + para('For Black/African and newcomer families, these experiences may also intersect with differences in culture, language, family structures, community expectations and lived experiences.')
        + "\n\n" + para('Inahitaji Kijiji Kulea Mtoto creates a bridge between families, community and available supports.', bold=True), content='900px'))
    pillars = [('Family Resilience Circles', '2026/09/Family-Resilience-Circles.png', 'Black African family, children, elders, and a community facilitator seated together in a supportive family resilience circle.', 'Strengthening families through collective support, healing and culturally grounded practices that build connection and resilience.'),
               ('Community Resource Navigation', '2026/09/Community-Resource-Navigation.png', 'Black African family meeting with a community worker to review practical supports and community resources.', 'Helping families connect with the services, supports, resources and opportunities they need to flourish.'),
               ('Community Education & Advocacy', '2026/09/Community-Education-and-Advocacy.png', 'Black African families and community members taking part in an empowering community education and advocacy workshop.', 'Promoting awareness, equity and systemic change within child-welfare and community systems.')]
    t.append(section(heading('Our village approach', 2, 'x-large', 'center') + "\n\n" + para('Our approach is built on three interconnected and culturally responsive pillars.', align='center')
        + "\n\n" + columns([column(image(U + p, a) + "\n\n" + heading(h, 3, 'large') + "\n\n" + para(x), 'top') for h, p, a, x in pillars], 'top')))
    aud = [('Black/African families', 'Families in Hamilton who are currently engaging with the child-welfare system and may benefit from culturally responsive community support.'),
           ('Newcomer families', 'Parents and caregivers who may be navigating both a new country and an unfamiliar child- and family-support system.'),
           ('Parents & caregivers', 'Families seeking information, connection, culturally grounded support and easier access to community resources.'),
           ('Extended family & community', 'Grandparents, relatives, elders and trusted community members who form part of the village around a child.')]
    t.append(section(heading('Who is this program for?', 2, 'x-large') + "\n\n" + para('This program is being developed with our community in mind. The primary audience is Black/African and newcomer families in Hamilton who are navigating the child-welfare system.')
        + "\n\n" + card_grid(aud, 2)
        + "\n\n" + heading('Are you a community or service professional?', 3, 'large') + "\n\n" + para('Community leaders, service providers, family-support professionals and organizations interested in supporting Black/African families are also invited to learn about the initiative and connect with HBHCLF.'), bg='black', text='white'))
    why = [('Representation & Equity', 'Responding to the overrepresentation and disparity experienced by Black/African children and families within child welfare.'),
           ('Culturally informed support', 'Encouraging approaches that recognize culture, identity, lived experience and community.'),
           ('Family & community resilience', 'Strengthening the networks around children so families and communities have greater capacity to support them over the long term.')]
    t.append(section(heading('Why this matters', 2, 'x-large') + "\n\n" + heading('Every child deserves the opportunity to flourish without losing connection to family, culture and community.', 3, 'large') + "\n\n" + card_grid(why, 3)))
    diff = [('Community-led', 'Designed around the strengths, realities and voices of the community.'), ('Culturally responsive', 'Recognizing that identity, culture and family structures matter.'), ('Family-centred', 'Looking beyond individual challenges to the strength and well-being of the whole family.'),
            ('Wrap-around support', 'Connecting families to multiple forms of community support rather than treating challenges in isolation.'), ('Navigation & connection', 'Helping make community resources and support easier to understand and access.'), ('Advocacy for change', 'Supporting greater equity within the systems that serve Black/African children and families.')]
    t.append(section(heading('What makes this different?', 2, 'x-large') + "\n\n" + card_grid(diff, 3), bg='green', text='black'))
    t.append(section(heading('It takes a village', 2, 'x-large', 'center') + "\n\n" + heading('Children flourish when the people around them flourish too.', 3, 'large', 'center')
        + "\n\n" + para('A child needs parents and caregivers. But families also need communities. Communities need resources. And systems need to understand the people they serve.', align='center')
        + "\n\n" + para('That is the village we are working to strengthen.', bold=True, align='center'), content='900px'))
    vol = (kicker('Now recruiting: volunteer opportunity', 'amber') + "\n\n" + heading('Volunteer opportunity: ABUSUA/Elder Volunteer', 2, 'x-large') + "\n\n" + heading('It Takes a Village to Raise a Child', 3, 'large') + "\n\n" + para('Supporting African/Black Families and Youth')
        + "\n\n" + lst(['Role type: Volunteer position with an honorarium', 'Program: It Takes a Village to Raise a Child', 'Location: Hamilton, Ontario; community, virtual and program locations as required', 'Reports to: Program Manager/Designate', 'Primary participants: African/Black parents, caregivers, families and youth'])
        + "\n\n" + heading('About the program', 3, 'large') + "\n\n" + para('It Takes a Village to Raise a Child strengthens cultural connections, access to resources and community-based circles of care for African/Black families and youth who are involved with the Hamilton Child and Family Supports.')
        + "\n\n" + heading('Role summary', 3, 'large') + "\n\n" + para('The ABUSUA/Elder Volunteer is a respected community member who shares cultural knowledge, lived experience and guidance with parents, caregivers, families and youth. The volunteer facilitates parenting-in-the-diaspora sessions, culturally grounded circles and consultations; connects participants with supports; and promotes awareness of African/Black foster care through town halls and community engagement. The role supports family and youth well-being, cultural identity, belonging and collective responsibility. Volunteers receive an honorarium recognizing their time, knowledge and contribution.')
        + "\n\n" + heading('Key responsibilities', 3, 'large') + "\n\n" + para('Provide parenting information, cultural circles and consultation', bold=True)
        + "\n\n" + lst(['Plan, facilitate or co-facilitate accessible, culturally responsive parenting-in-the-diaspora sessions for parents and caregivers.', 'Share practical knowledge and create respectful discussion about identity, belonging, intergenerational relationships, discipline, communication, education, child development and navigating Canadian systems.', 'Facilitate culturally appropriate or restorative circles where families and youth can speak, listen, reflect and seek guidance without judgment.', 'Offer cultural consultation on values, traditions, family structures and community practices while respecting diverse cultures, faiths, identities and perspectives.', 'Promote peer learning, family and youth voice, healing, resilience, cultural connection and belonging.'])
        + "\n\n" + heading('Desired qualifications and attributes', 3, 'large') + "\n\n" + lst(['Trusted standing in, or a meaningful connection to, African, Black, racialized and/or newcomer communities.', 'Relevant lived experience, cultural knowledge or community wisdom related to parenting, caregiving, youth development or diaspora family life.', 'Experience supporting families or youth and contributing to groups, circles, information sessions, town halls or community gatherings.', 'Strong listening, communication and relationship-building skills, with empathy, patience, cultural humility and a non-judgmental approach.', 'Understanding of anti-Black racism, systemic barriers and migration-related challenges affecting the communities served.', 'Commitment to child and youth well-being, family voice, cultural identity and community-based care.', 'Reliability, teamwork, confidentiality and appropriate personal and professional boundaries.'])
        + "\n\n" + heading('Additional assets', 3, 'large') + "\n\n" + lst(['Experience facilitating cultural, restorative, healing or community circles.', 'Knowledge of Hamilton services and African, Black, racialized or newcomer community networks.', 'Experience in foster or kinship care, child and family services, settlement, education, health or community development.', 'Fluency in a language spoken by the communities served.', 'Training in facilitation, mental-health first aid, conflict resolution, trauma-informed practice or crisis response.', 'Comfortable speaking at town halls and public education events.'])
        + "\n\n" + heading('Time commitment and honorarium', 3, 'large') + "\n\n" + lst(['Flexible, part-time participation based on program and community needs, including sessions, circles, consultations, family support, meetings and town halls.', 'Some evening or weekend participation may be required.', 'Volunteers receive an honorarium; the program will communicate the amount, schedule and requirements. The honorarium does not create an employment relationship.'])
        + "\n\n" + heading('How to apply', 3, 'large') + "\n\n" + para('Please send your resume to <a href="mailto:info@hbhclf.org?subject=ABUSUA/Elder%20Volunteer%20Application">info@hbhclf.org</a> as soon as possible.', raw=True)
        + "\n\n" + button('Apply now: register to volunteer', '#volunteer-form', orange=True))
    t.append(section(vol, content='900px', bg='black', text='white', anchor='volunteer'))
    t.append(section(heading('Register to volunteer as an ABUSUA/Elder', 2, 'x-large') + "\n\n" + shortcode('[fluentform id="7"]'), content='800px', anchor='volunteer-form'))
    t.append(section(heading('Be among the first to know', 2, 'x-large', 'center') + "\n\n" + para('Inahitaji Kijiji Kulea Mtoto is coming soon to Hamilton.', 'large', align='center')
        + "\n\n" + para('We are preparing to welcome families and community members into this new initiative. Join the HBHCLF mailing list for launch updates, or contact us if you would like to learn more about family support or community partnership opportunities.', align='center')
        + "\n\n" + buttons([('Get program updates', '/join-our-mailing-list/'), ('I’m interested in family support', '/contact-us/'), ('I’m a community or service partner', '/contact-us/')]).replace('<div class="wp-block-buttons">', '<div class="wp-block-buttons">', 1), bg='orange', text='black', content='900px'))
    faq = [('What is Inahitaji Kijiji Kulea Mtoto?', 'It is an upcoming HBHCLF community-led wrap-around support initiative for racialized Black/African and newcomer families in Hamilton who are engaged with the child-welfare system.'),
           ('Who is the program for?', 'The program is intended for racialized Black/African and newcomer families in Hamilton who are navigating the child-welfare system.'),
           ('What support will the program focus on?', 'Its three interconnected pillars are Family Resilience Circles, Community Resource Navigation, and Community Education & Advocacy.'),
           ('When does the program begin?', 'The program is coming soon. Join the HBHCLF mailing list to receive updates when launch information becomes available.')]
    det = "\n\n".join(f'<!-- wp:details -->\n<details class="wp-block-details"><summary>{e(q)}</summary><!-- wp:paragraph -->\n<p>{e(a)}</p>\n<!-- /wp:paragraph --></details>\n<!-- /wp:details -->' for q, a in faq)
    t.append(section(heading('Frequently asked questions', 2, 'x-large') + "\n\n" + det, content='900px'))
    t.append(section(heading('When a child thrives, a family grows stronger.', 2, 'x-large', 'center') + "\n\n" + heading('When families grow stronger, communities flourish.', 3, 'large', 'center')
        + "\n\n" + para('Inahitaji Kijiji Kulea Mtoto: coming soon to Hamilton.', bold=True, align='center') + "\n\n" + button('Keep me updated', '/join-our-mailing-list/', orange=True, center=True), bg='black', text='white', content='900px'))
    write('inahitaji.html', t)

if __name__ == '__main__':
    about(); programs(); gallery(); contact(); newcomers(); inahitaji()
    for f in sorted(os.listdir(OUT)):
        s = open(os.path.join(OUT, f)).read()
        print(f.ljust(32), len(s), 'chars', s.count('<!-- wp:'), 'blocks')
