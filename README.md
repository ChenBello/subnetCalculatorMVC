# Subnet Calculator MVC

This project is a Subnet Calculator implemented using the MVC pattern in C#. It includes two different versions of the subnet calculator:

- **finalCalcBasedOnNetworkClasses**  
  A calculator based on traditional network classes (Classful Networking) — divides IP addresses into Classes A, B, and C and calculates subnets accordingly.

- **finalNotBasedOnNetworkClasses**  
  A calculator based on Classless Inter-Domain Routing (CIDR) — allows flexible subnet calculations using custom subnet masks.

## Project Structure

- **Models** — contains the core business logic and subnet calculation algorithms.
- **Views** — user interface for input and displaying results.
- **Controllers** — handle communication between Models and Views.

## How it Works

The classful version follows the classic division of IP addresses into classes with fixed subnet masks. For example, Class A uses 8 bits for the network and 24 bits for hosts.

The CIDR-based version ignores classes and calculates subnet masks dynamically, allowing for more efficient use of IP address space.

## Requirements

- .NET Framework 4.7.2 or higher
- Visual Studio 2019/2022 or any MVC-compatible IDE

## Running the Project

1. Open the solution in Visual Studio.
2. Choose either the `finalCalcBasedOnNetworkClasses` or the `finalNotBasedOnNetworkClasses` folder, depending on which version you want to run.
3. Build and run the application.
4. Enter an IP address, subnet mask, or other required parameters depending on the version.
5. View the calculated subnet details.

---

If you want help with deployment, usage tips, or explanations on subnetting concepts, just ask!
