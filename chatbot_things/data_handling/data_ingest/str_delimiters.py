
slice_dict = {
    "Address": ("@ Address:", "@ Beginning date of Lease (Par. 3)"),
    "beginning date": ("@ Beginning date of Lease (Par. 3)", "Number of days notice for termination"),
    "termination notice": ("@ Number of days notice for termination (Par. 3)", "security deposit (Par. 4)"),
    "security deposit 1": ("security deposit (Par. 4)", "@ Ending date of Lease (Par. 3)"),
    "end date": ("@ Ending date of Lease (Par. 3)", "Consent for guests"),
    "guest stays": ("Consent for guests", "(Par. 2)"),
    "pet deposit": ("Animal deposit (if any)", "@ Security deposit"),
    "pet security deposit": ("Security deposit (Par. 4)", "@ Security deposit"),#0 does OR & does not include an animal deposit.

    "refund check": ("(Par. 4) (check one)", "# of keys/access devices"), # & one check jointly payable to all residents (default),\n\nORO one check payable to and mailed to\n\n@ 


    "keys/ access": ("@ # of keys/access devices", "will terminate Lease on (Par. 5): (check one)"), #& last day of month OR 0 exact day designated in notice
    "included in rent": ("included in monthly rent:", "Total monthly rent (Par. 6)"), #Check here if included in monthly rent: 0 garage, 0 storage, 0) carport, 0 washer/dryer, or 0 other\n\n# Total monthly rent (Par. 6) 
    "total rent": ("Total monthly rent (Par. 6)", "Bf Late fees if rent is not paid on or before"),
    "begin late fee": ("Bf Late fees if rent is not paid on or before (Par. 6) ", "@ Returned-check charge"),
    "bounced check ": ("@ Returned-check charge (Par. 6)", "# Monthly animal rent (if any)"),
    "animal rent": ("# Monthly animal rent (if any)", "# Monthly pest control (if any)"),
    "pest control": ("# Monthly pest control (if any)", "Repair or service call fee"),
    "repairman": ("@ Repair or service call fee (Par. 6)", "H Prorated rent (Par. 6) for (check one)"),
    "prorated": ("Prorated rent (Par. 6) for (check one)", "Hf Daily late fee"), #O first month ORO secondmonth 
    "daily late fee": ("Daily late fee (Par. 6) ", "H Animal violation charges (Par. 27)"),
    "animal violation": ("H Animal violation charges (Par. 27)", "@ Monthly trash / waste (if any)"),
    "trash": ("@ Monthly trash / waste (if any)", "$\n\n@ Who provides trash receptacle (Par. 12): (check one) "), #& you, 0 us, O city utility, 0 other\n@ ,
    "replace trash can": ("Who replaces broken or missing trash receptacle (Par. 12): (check one)", "\n\n# Utility"), #% you OR Ous\
    "chatbot_things/utilities": ("Utility connection charge (Par. 12)", "@ Agreed reletting charge (Par. 10)"),
    "reletting": ("@ Agreed reletting charge (Par. 10)", "H@ You are: (check one) "),
    "insurance": ("H@ You are: (check one) ", "(Par. 8)\n\n@ Special provisions "),
    "provisions": ("(Par. 8)\n\n@ Special provisions (Par.9):", "\n\nSignatures and Attachments"),
    "signed": ("\nDOCUMENT", None),
}
