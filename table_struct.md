
Flow 
----------------------------------------------------------
|-> Login = {

}
|-> signup = {

}



Roles : Admin, members, 

Admin => Chapter creater
Members => Joiner

Chapter => {
    "Role" : []
}


------------------------------------------------------------
profile = {
    Display Name,
    Role, = > Important
    Bio,
    Chapters(Groups), => need to create separate Table
    Connections, => need to create  a new table for connections.
    gender,
    Birth Date,
    Address,
    Email,
    Industry,
    My Business = "Able to show the ckeditor details into profile",
}

---------------------------------------------------------

Connections_flow = {
    "profile llistout",
    "Add New Connections by searching in globally"
}
Connection_table = {
    "User_id" : "Connected User_id",
    "Status" : ["Pending","Accepted","Rejected"],
    
}