---
source_url: https://en.wikipedia.org/wiki/Design_by_contract
ingested: 2026-06-15
---
![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Design_by_contract.svg/250px-Design_by_contract.svg.png)

A design by contract scheme

**Design by contract** (**DbC**), also known as **contract programming**, **programming by contract** and **design-by-contract programming**, is an approach for [designing software](https://en.wikipedia.org/wiki/Software_design "Software design").

It prescribes that software designers should define [formal](https://en.wikipedia.org/wiki/Formal_methods "Formal methods"), precise and verifiable interface specifications for [software components](https://en.wikipedia.org/wiki/Component-based_software_engineering#Software_component "Component-based software engineering"), which extend the ordinary definition of [abstract data types](https://en.wikipedia.org/wiki/Abstract_data_type "Abstract data type") with [preconditions](https://en.wikipedia.org/wiki/Precondition "Precondition"), [postconditions](https://en.wikipedia.org/wiki/Postcondition "Postcondition") and [invariants](https://en.wikipedia.org/wiki/Invariant_\(computer_science\) "Invariant (computer science)"). These specifications are referred to as "contracts", in accordance with a [conceptual metaphor](https://en.wikipedia.org/wiki/Conceptual_metaphor "Conceptual metaphor") with the conditions and obligations of business contracts.

The DbC approach [assumes](https://en.wikipedia.org/wiki/Offensive_programming "Offensive programming") all *client components* that invoke an operation on a *server component* will meet the preconditions specified as required for that operation.

Where this assumption is considered too risky (as in multi-channel or [distributed computing](https://en.wikipedia.org/wiki/Distributed_computing "Distributed computing")), the [inverse approach](https://en.wikipedia.org/wiki/Defensive_programming "Defensive programming") is taken, meaning that the *server component* tests that all relevant preconditions hold true (before, or while, processing the *client component'* s request) and replies with a suitable error message if not.

## History

The term was coined by [Bertrand Meyer](https://en.wikipedia.org/wiki/Bertrand_Meyer "Bertrand Meyer") in connection with his design of the [Eiffel programming language](https://en.wikipedia.org/wiki/Eiffel_\(programming_language\) "Eiffel (programming language)") and first described in various articles starting in 1986 [^1] [^2] [^3] and the two successive editions (1988, 1997) of his book *[Object-Oriented Software Construction](https://en.wikipedia.org/wiki/Object-Oriented_Software_Construction "Object-Oriented Software Construction")*. Eiffel Software applied for trademark registration for *Design by Contract* in December 2003, and it was granted in December 2004.[^4] [^5] The current owner of this trademark is Eiffel Software.[^6] [^7]

Design by contract has its roots in work on [formal verification](https://en.wikipedia.org/wiki/Formal_verification "Formal verification"), [formal specification](https://en.wikipedia.org/wiki/Formal_specification "Formal specification") and [Hoare logic](https://en.wikipedia.org/wiki/Hoare_logic "Hoare logic"). The original contributions include:

- A clear metaphor to guide the design process
- The application to [inheritance](https://en.wikipedia.org/wiki/Inheritance_\(object-oriented_programming\) "Inheritance (object-oriented programming)"), in particular a formalism for redefinition and [dynamic binding](https://en.wikipedia.org/wiki/Dynamic_binding_\(computer_science\) "Dynamic binding (computer science)")
- The application to [exception handling](https://en.wikipedia.org/wiki/Exception_\(computer_science\) "Exception (computer science)")
- The connection with automatic [software documentation](https://en.wikipedia.org/wiki/Software_documentation "Software documentation")

## Description

The central idea of DbC is a metaphor on how elements of a software system collaborate with each other on the basis of mutual *obligations* and *benefits*. The metaphor comes from business life, where a "client" and a "supplier" agree on a "contract" that defines, for example, that:

- The supplier must provide a certain product (obligation) and is entitled to expect that the client has paid its fee (benefit).
- The client must pay the fee (obligation) and is entitled to get the product (benefit).
- Both parties must satisfy certain obligations, such as laws and regulations, applying to all contracts.

Similarly, if the [method](https://en.wikipedia.org/wiki/Method_\(computer_science\) "Method (computer science)") of a [class](https://en.wikipedia.org/wiki/Class_\(programming\) "Class (programming)") in [object-oriented programming](https://en.wikipedia.org/wiki/Object-oriented_programming "Object-oriented programming") provides a certain functionality, it may:

- Expect a certain condition to be guaranteed on entry by any client module that calls it: the method's [precondition](https://en.wikipedia.org/wiki/Precondition "Precondition") —an obligation for the client, and a benefit for the supplier (the method itself), as it frees it from having to handle cases outside of the precondition.
- Guarantee a certain property on exit: the method's [postcondition](https://en.wikipedia.org/wiki/Postcondition "Postcondition") —an obligation for the supplier, and obviously a benefit (the main benefit of calling the method) for the client.
- Maintain a certain property, assumed on entry and guaranteed on exit: the [class invariant](https://en.wikipedia.org/wiki/Class_invariant "Class invariant").

The contract is semantically equivalent to a [Hoare triple](https://en.wikipedia.org/wiki/Hoare_triple "Hoare triple") which formalises the obligations. This can be summarised by the "three questions" that the designer must repeatedly answer in the contract:

- What does the contract expect?
- What does the contract guarantee?
- What does the contract maintain?

Many [programming languages](https://en.wikipedia.org/wiki/Programming_language "Programming language") have facilities to make [assertions](https://en.wikipedia.org/wiki/Assertion_\(software_development\) "Assertion (software development)") like these. However, DbC considers these contracts to be so crucial to [software correctness](https://en.wikipedia.org/wiki/Correctness_\(computer_science\) "Correctness (computer science)") that they should be part of the design process. In effect, DbC advocates [writing the assertions first](https://en.wikipedia.org/wiki/Test-driven_development "Test-driven development"). Contracts can be written by [code comments](https://en.wikipedia.org/wiki/Comment_\(computer_programming\) "Comment (computer programming)"), enforced by a [test suite](https://en.wikipedia.org/wiki/Test_suite "Test suite"), or both, even if there is no special language support for contracts.

The notion of a contract extends down to the method/procedure level; the contract for each method will normally contain the following pieces of information:

- Acceptable and unacceptable input values or types, and their meanings
- Return values or types, and their meanings
- Error and [exception](https://en.wikipedia.org/wiki/Exception_handling "Exception handling") condition values or types that can occur, and their meanings
- [Side effects](https://en.wikipedia.org/wiki/Side_effect_\(computer_science\) "Side effect (computer science)")
- [Preconditions](https://en.wikipedia.org/wiki/Precondition "Precondition")
- [Postconditions](https://en.wikipedia.org/wiki/Postcondition "Postcondition")
- [Invariants](https://en.wikipedia.org/wiki/Invariant_\(computer_science\) "Invariant (computer science)")
- (more rarely) Performance guarantees, e.g. for time or space used

Subclasses in an [inheritance hierarchy](https://en.wikipedia.org/wiki/Inheritance_\(object-oriented_programming\) "Inheritance (object-oriented programming)") are allowed to weaken preconditions (but not strengthen them) and strengthen postconditions and invariants (but not weaken them). These rules approximate [behavioural subtyping](https://en.wikipedia.org/wiki/Liskov_substitution_principle "Liskov substitution principle").

All class relationships are between client classes and supplier classes. A client class is obliged to make calls to supplier features where the resulting state of the supplier is not violated by the client call. Subsequently, the supplier is obliged to provide a return state and data that does not violate the state requirements of the client.

For instance, a supplier data buffer may require that data is present in the buffer when a delete feature is called. Subsequently, the supplier guarantees to the client that when a delete feature finishes its work, the data item will, indeed, be deleted from the buffer. Other design contracts are concepts of [class invariant](https://en.wikipedia.org/wiki/Class_invariant "Class invariant"). The class invariant guarantees (for the local class) that the state of the class will be maintained within specified tolerances at the end of each feature execution.

When using contracts, a supplier will verify that the contract conditions are satisfied—a practice known as [offensive programming](https://en.wikipedia.org/wiki/Offensive_programming "Offensive programming") —the general idea being that code should "fail hard", with contract verification being the safety net.

DbC's "fail hard" property simplifies the debugging of contract behavior, as the intended behaviour of each method is clearly specified.

This approach differs substantially from that of [defensive programming](https://en.wikipedia.org/wiki/Defensive_programming "Defensive programming"), where the supplier is responsible for figuring out what to do when a precondition is broken. More often than not, the supplier throws an exception to inform the client that the precondition has been broken, and in both cases—DbC and defensive programming alike—the client must figure out how to respond to that. In such cases, DbC makes the supplier's job easier.

Design by contract also defines criteria for correctness for a software module:

- If the class invariant AND precondition are true before a supplier is called by a client, then the invariant AND the postcondition will be true after the service has been completed.
- When making calls to a supplier, a software module should not violate the supplier's preconditions.

Design by contract can also facilitate code reuse, since the contract for each piece of code is fully documented. The contracts for a module can be regarded as a form of [software documentation](https://en.wikipedia.org/wiki/Software_documentation "Software documentation") for the behavior of that module.

Design by contract, in C++ for example, looks like the following:[^8] [^9]

```
int f(const int x)
    pre(x != 1) // a precondition assertion
    post(r : r == x && r != 2) // a postcondition assertion; r names the result object of f
{
    contract_assert(x != 3); // an assertion statement
    return x;
}
```

## Performance implications

Contract conditions should never be violated during execution of a bug-free program. Contracts are therefore typically only checked in debug mode during software development. Later at release, the contract checks are disabled to maximize performance.

In many programming languages, contracts are implemented with [assert](https://en.wikipedia.org/wiki/Assertion_\(software_development\) "Assertion (software development)"). Asserts are by default compiled away in release mode in C/C++, and similarly deactivated in C# [^10] and Java.

Launching the Python interpreter with "-O" (for "optimize") as an argument will likewise cause the Python code generator to not emit any bytecode for asserts.[^11]

This effectively eliminates the run-time costs of asserts in production code—irrespective of the number and computational expense of asserts used in development—as no such instructions will be included in production by the compiler.

## Relationship to software testing

Design by contract does not replace regular testing strategies, such as [unit testing](https://en.wikipedia.org/wiki/Unit_testing "Unit testing"), [integration testing](https://en.wikipedia.org/wiki/Integration_testing "Integration testing") and [system testing](https://en.wikipedia.org/wiki/System_testing "System testing"). Rather, it complements external testing with internal self-tests that can be activated both for isolated tests and in production code during a test-phase.

The advantage of internal self-tests is that they can detect errors before they manifest themselves as invalid results observed by the client. This leads to earlier and more specific error detection.

The use of assertions can be considered to be a form of [test oracle](https://en.wikipedia.org/wiki/Test_oracle "Test oracle"), a way of testing the design by contract implementation.

## Language support

### Languages with native support

Languages that implement most DbC features natively include:

- [Ada 2012](https://en.wikipedia.org/wiki/Ada_\(programming_language\) "Ada (programming language)")
	- [SPARK](https://en.wikipedia.org/wiki/SPARK_\(programming_language\) "SPARK (programming language)") (via [static analysis](https://en.wikipedia.org/wiki/Static_code_analysis "Static code analysis") of [Ada](https://en.wikipedia.org/wiki/Ada_\(programming_language\) "Ada (programming language)") programs)
- [Ciao](https://en.wikipedia.org/wiki/Ciao_\(programming_language\) "Ciao (programming language)")
- [Clojure](https://en.wikipedia.org/wiki/Clojure "Clojure")
- [Cobra](https://en.wikipedia.org/wiki/Cobra_\(programming_language\) "Cobra (programming language)")
- [C++](https://en.wikipedia.org/wiki/C%2B%2B "C++") (since [C++26](https://en.wikipedia.org/wiki/C%2B%2B26 "C++26")) [^9]
- [D](https://en.wikipedia.org/wiki/D_\(programming_language\) "D (programming language)") [^12]
- [Dafny](https://en.wikipedia.org/wiki/Dafny_\(programming_language\) "Dafny (programming language)")
- [Eiffel](https://en.wikipedia.org/wiki/Eiffel_\(programming_language\) "Eiffel (programming language)")
- [Fortress](https://en.wikipedia.org/wiki/Fortress_\(programming_language\) "Fortress (programming language)")
- [Kotlin](https://en.wikipedia.org/wiki/Kotlin "Kotlin")
- [Mercury](https://en.wikipedia.org/wiki/Mercury_\(programming_language\) "Mercury (programming language)")
- [Oxygene](https://en.wikipedia.org/wiki/Oxygene_\(programming_language\) "Oxygene (programming language)") (formerly Chrome and [Delphi](https://en.wikipedia.org/wiki/Delphi_\(software\) "Delphi (software)") Prism [^13])
- [Racket](https://en.wikipedia.org/wiki/Racket_\(programming_language\) "Racket (programming language)") (including higher order contracts, and emphasizing that contract violations must blame the guilty party and must do so with an accurate explanation [^14])
- [Sather](https://en.wikipedia.org/wiki/Sather "Sather")
- [Scala](https://en.wikipedia.org/wiki/Scala_\(programming_language\) "Scala (programming language)") [^15] [^16]
- [Vala](https://en.wikipedia.org/wiki/Vala_\(programming_language\) "Vala (programming language)")
- [Vienna Development Method](https://en.wikipedia.org/wiki/Vienna_Development_Method "Vienna Development Method") (VDM)

Further, the standard method combination in the [Common Lisp Object System](https://en.wikipedia.org/wiki/Common_Lisp_Object_System "Common Lisp Object System") has the method qualifiers `:before`, `:after` and `:around` that allow writing contracts as auxiliary methods, among other uses.

[^1]: Meyer, Bertrand: *Design by Contract*, Technical Report TR-EI-12/CO, Interactive Software Engineering Inc., 1986

[^2]: Meyer, Bertrand: *Design by Contract*, in *Advances in Object-Oriented Software Engineering*, eds. D. Mandrioli and B. Meyer, Prentice Hall, 1991, pp. 1–50

[^3]: Meyer, Bertrand: " [Applying "Design by Contract"](http://se.ethz.ch/~meyer/publications/computer/contract.pdf) ", in *Computer* (IEEE), 25, 10, October 1992, pp. 40–51.

[^4]: ["United States Patent and Trademark Office registration for "DESIGN BY CONTRACT""](https://web.archive.org/web/20161221062729/http://tess2.uspto.gov/bin/showfield?f=doc&state=4010:lsqmmo.2.2). Archived from [the original](http://tess2.uspto.gov/bin/showfield?f=doc&state=4010:lsqmmo.2.2) on 2016-12-21. Retrieved 2009-06-22.

[^5]: ["United States Patent and Trademark Office registration for the graphic design with words "Design by Contract""](https://web.archive.org/web/20161221062436/http://tess2.uspto.gov/bin/showfield?f=doc&state=4010:lsqmmo.2.1). Archived from [the original](http://tess2.uspto.gov/bin/showfield?f=doc&state=4010:lsqmmo.2.1) on 2016-12-21. Retrieved 2009-06-22.

[^6]: ["Trademark Status & Document Retrieval - 78342277"](http://tarr.uspto.gov/servlet/tarr?regser=serial&entry=78342277). *USPTO Trademark Application and Registration Retrieval*.

[^7]: ["Trademark Status & Document Retrieval - 78342308"](http://tarr.uspto.gov/servlet/tarr?regser=serial&entry=78342308). *USPTO Trademark Application and Registration Retrieval*.

[^8]: Joshua Berne; Timur Doumler; Andrzej Krzemieński (13 February 2025). ["Contracts for C++"](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2900r14.pdf) (PDF). *open-std.org*. WG 22.

[^9]: ["Contract assertions (since C++26)"](https://en.cppreference.com/w/cpp/language/contracts.html). *cppreference.com*. cppreference. Retrieved 9 November 2025.

[^10]: ["Assertions in Managed Code"](https://msdn.microsoft.com/en-us/library/ttcc4x86.aspx). *Microsoft Developer Network*. 15 November 2016. [Archived](https://web.archive.org/web/20180822105637/https://msdn.microsoft.com/en-us/library/ttcc4x86.aspx) from the original on Aug 22, 2018.

[^11]: [Official Python Docs, *assert statement*](https://docs.python.org/3/reference/simple_stmts.html#grammar-token-assert-stmt)

[^12]: Bright, Walter (2014-11-01). ["D Programming Language, Contract Programming"](http://dlang.org/contracts.html). Digital Mars. Retrieved 2014-11-10.

[^13]: Hodges, Nick. ["Write Cleaner, Higher Quality Code with Class Contracts in Delphi Prism"](https://web.archive.org/web/20210426163433/https://edn.embarcadero.com/article/39398). Embarcadero Technologies. Archived from [the original](http://edn.embarcadero.com/article/39398) on 26 April 2021. Retrieved 20 January 2016.

[^14]: Findler, Felleisen [Contracts for Higher-Order Functions](http://www.eecs.northwestern.edu/~robby/pubs/papers/ho-contracts-icfp2002.pdf)

[^15]: ["Scala Standard Library Docs - Assertions"](https://www.scala-lang.org/api/current/scala/Predef$.html). EPFL. Retrieved 2019-05-24.

[^16]: [Strong typing](https://en.wikipedia.org/wiki/Strong_typing "Strong typing") as another "contract enforcing" in Scala, see discussion at [scala-lang.org/](https://www.scala-lang.org/old/node/6958).