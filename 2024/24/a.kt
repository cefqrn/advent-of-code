/*
    https://kotlinlang.org/docs/
    https://learnxinyminutes.com/kotlin/
    https://stackoverflow.com/questions/63285907/how-does-a-extension-method-work-in-kotlin
    https://kotlinlang.org/docs/command-line.html
    https://stackoverflow.com/questions/55182578/how-to-read-plain-text-file-in-kotlin
    https://docs.oracle.com/javase/8/docs/api/java/util/Formatter.html

    run with 
        kotlinc -include-runtime -d a.jar a.kt && java -jar a.jar
 */

import java.io.File

fun main() {
    val f = File("input")
    val lines = f.readLines().asSequence()

    val initial = mutableMapOf<String, Int>()
    lines.takeWhile{!it.isBlank()}.forEach {
        val (gate: String, v: String) = it.split(": ")
        initial[gate] = v.toInt()
    }

    val gates = mutableMapOf<String, Gate>()
    lines.drop(initial.size + 1).forEach {
        val (l, opStr, r, _, name) = it.split(" ")
        gates[name] = Gate(opStr.toOperator(), l, r)
    }

    println(getn(initial, gates, "z"))
    println(solve(initial, gates)!!.sorted().joinToString(","))
}

fun solve(initial: Map<String, Int>, gates: MutableMap<String, Gate>, maxSwaps: Int=4): List<String>? {
    // could move target calculation out since it doesn't change
    val x = getn(initial, gates, "x")!!
    val y = getn(initial, gates, "y")!!

    val target = x + y

    val z = getn(initial, gates, "z") ?: return null
    if (z == target) {
        return listOf()
    }

    if (maxSwaps == 0) {
        return null
    }

    var swappable = gates.keys.toSet()
    var correct = 0

    var gateName = "z%02d".format(correct)
    var gate = gates[gateName]!!
    var inputs = gate.getInputs(initial, gates)

    while (validateZ(initial, gates, gate, correct)) {
        swappable = swappable.subtract(inputs.union(setOf(gateName)))

        correct++

        gateName = "z%02d".format(correct)
        gate = gates[gateName]!!
        inputs = gate.getInputs(initial, gates)
    }

    // try swapping out the incorrect wire
    for (o in swappable.filter {it != gateName}.filter {validateZ(initial, gates, gates[it]!!, correct)}) {
        swap(gates, gateName, o)
        val otherSwaps = solve(initial, gates, maxSwaps - 1)
        swap(gates, o, gateName)

        if (otherSwaps != null) {
            return listOf(o, gateName) + otherSwaps
        }
    }

    // try swapping out one of its inputs
    for (a in inputs.intersect(swappable)) {
        for (b in swappable.filter {it != a}) {
            swap(gates, a, b)
            val newZ = gate.evaluate(initial, gates)
            var otherSwaps: List<String>? = null
            if (newZ != null && newZ.toLong() xor (target shr correct).lsb == 0L) {
                otherSwaps = solve(initial, gates, maxSwaps - 1)
            }
            swap(gates, b, a)

            if (otherSwaps != null) {
                return listOf(a, b) + otherSwaps
            }
        }
    }

    return null
}

fun validateZ(initial: Map<String, Int>, gates: Map<String, Gate>, z: Gate, i: Int): Boolean {
    if (i < 2) {
        return true
    }

    val counts = z.countOps(initial, gates)
    return when {
        counts[And]!! != 2*i-1 -> false
        counts[Or ]!! != i-1   -> false
        counts[Xor]!! != i+1   -> false
        else -> true
    }
}

fun swap(gates: MutableMap<String, Gate>, a: String, b: String) {
    val tmp = gates[b]!!
    gates[b] = gates[a]!!
    gates[a] = tmp
}

fun getn(initial: Map<String, Int>, gates: Map<String, Gate>, n: String): Long? {
    var value = 0L
    var i = 0
    while (true) {
        val gate = "%s%02d".format(n, i)
        val b = when (gate) {
            in initial -> initial[gate]!!
            in gates -> gates[gate]!!.evaluate(initial, gates) ?: return null
            else -> return value
        }.toLong()

        value += b shl i

        i++
    }
}

data class Gate(val op: Operator, val l: String, val r: String) {
    fun countOps(initial: Map<String, Int>, gates: Map<String, Gate>, seen: Set<String>?=null): Map<Operator, Int> {
        val newSeen = seen?.toMutableSet() ?: mutableSetOf()

        val counts = mutableMapOf<Operator, Int>(And to 0, Or to 0, Xor to 0)
        counts[op] = 1

        if (l !in initial && l !in newSeen) {
            newSeen.add(l)
            for ((k, v) in gates[l]!!.countOps(initial, gates, newSeen)) {
                counts[k] = counts[k]!! + v
            }
        }

        if (r !in initial && r !in newSeen) {
            newSeen.add(r)
            for ((k, v) in gates[r]!!.countOps(initial, gates, newSeen)) {
                counts[k] = counts[k]!! + v
            }
        }

        return counts
    }

    fun getInputs(initial: Map<String, Int>, gates: Map<String, Gate>, seen: Set<String>?=null): Set<String> {
        val newSeen = seen?.toMutableSet() ?: mutableSetOf()

        if (l !in initial && l !in newSeen) {
            newSeen.add(l)
            newSeen.addAll(gates[l]!!.getInputs(initial, gates, newSeen))
        }

        if (r !in initial && r !in newSeen) {
            newSeen.add(r)
            newSeen.addAll(gates[r]!!.getInputs(initial, gates, newSeen))
        }

        return newSeen
    }

    fun evaluate(initial: Map<String, Int>, gates: Map<String, Gate>, seen: Set<String>?=null): Int? {
        val inputs = setOf(l, r)
        val newSeen = seen?.union(inputs) ?: inputs
        if (newSeen.size < (seen?.size ?: 0) + 2) {
            return null
        }

        val lv = initial[l] ?: gates[l]!!.evaluate(initial, gates, newSeen) ?: return null
        val rv = initial[r] ?: gates[r]!!.evaluate(initial, gates, newSeen) ?: return null

        return op.evaluate(lv, rv) 
    }

    override fun toString() = "$l $op $r"
}

interface Operator {
    fun evaluate(l: Int, r: Int): Int
}

object And : Operator { override fun evaluate(l: Int, r: Int) = l and r }
object Or  : Operator { override fun evaluate(l: Int, r: Int) = l or  r }
object Xor : Operator { override fun evaluate(l: Int, r: Int) = l xor r }

fun String.toOperator(): Operator = when (this) {
    "AND" -> And
    "OR"  -> Or
    "XOR" -> Xor
    else -> error("unknown operator: '$this'")
}

val Long.lsb get() = this and 1L
