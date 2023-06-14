'''Defines the schema of which sections of the pdf to preserve'''

SECTIONS: list = [# Each pair is a section to extract
        # The first element is the beginning string, and  # second element is the ending string
        # bed bug addenda
        ['This Lease Contract (“Lease”) is between you, the resident(s) as listed below and u', "Special Provisions"],
        ["Bed Bug Addendum", "confirmation of bed-bug presence by a licensed pest-control"],
        ["Resident or Residents (all sign below) Owner or Owner's Representative (sign below)", "(Name of Resident) Date signed"],
        # insurance addendum
        ["INSURANCE ADDENDUM", "Owner does not acquire or maintain insurance for Resident's benefit"],
        ["THE REQUIRED INSURANCE POLICY UNDER THIS ADDENDUM", "Texas Apartment Association"],
        # texas apartment association
        ["TEXAS APARTMEN'T ASSOCIATION", " 2 The reletting charge is not a cancellation fee"],
        # animals
        ["violate the animal restrictions", "deodorizing, and shampooing"],
        # summary of key info
        ["SUMMARY OF KEY INFORMATION", "3Revised October 2019 Page8of8"],
        # mold
        ["Mold Information and Prevention Addendum", "About Mold."],["any signs of water leaks", "statewide Form 15-FF"],
        # military
        ["FOR MILITARY PERSONNEL", "Date of TAA Lease Contract"],
        # smoking
        ["NO SMOKING LEASE ADDENDUM", "25 feet from the buildings"],
        # all addenda
        ["Total Pages", ""],
        ["DOCUMENT AUDIT CONTINUED", ""]   
    ]
