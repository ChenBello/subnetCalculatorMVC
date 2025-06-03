# Subnet Calculator MVC

This project is a Subnet Calculator implemented using the MVC pattern in Python. It includes two versions of the subnet calculator:

- **finalCalcBasedOnNetworkClasses**  
  Calculates subnets based on traditional network classes (Classful Networking), dividing IP addresses into Classes A, B, and C with fixed subnet masks.

- **finalNotBasedOnNetworkClasses**  
  Uses Classless Inter-Domain Routing (CIDR) for flexible subnet calculations with custom subnet masks.

## Project Structure

- **Models** - contains the core logic for subnet calculations.  
- **Views** - handles user input and displays results.  
- **Controllers** - connects Models and Views, managing data flow.

## How Subnet Calculations Work

### Classful Networking (Network Classes)

In this version, IP addresses are divided into fixed classes:

- **Class A:** Network part uses 8 bits, host part uses 24 bits  
- **Class B:** Network part uses 16 bits, host part uses 16 bits  
- **Class C:** Network part uses 24 bits, host part uses 8 bits  

Subnet masks are fixed according to the class, and subnetting splits the host bits into subnets and hosts per subnet.

### CIDR-Based Networking

This version ignores fixed classes and allows subnet masks of any length. It calculates:

- Number of subnets possible (based on borrowed bits from host portion)  
- Number of hosts per subnet (based on remaining host bits)  
- Network address, broadcast address, and valid host ranges  

Using CIDR gives more efficient use of IP space, allowing networks to be sized flexibly.

## How to Run

1. Open the project in PyCharm or any Python IDE.  
2. Choose the folder for the version you want:  
   - `finalCalcBasedOnNetworkClasses` or  
   - `finalNotBasedOnNetworkClasses`  
3. Run the main script.  
4. Enter the required input (IP address, subnet mask, etc.) as prompted.  
5. View the subnet details calculated and displayed.

---

If you want help with deployment, usage, or subnetting concepts, feel free to ask!
