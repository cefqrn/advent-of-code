/*
    https://learnxinyminutes.com/csharp/
    https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-specification/expressions#1243-operator-overloading
    https://stackoverflow.com/a/14115783
    https://learn.microsoft.com/en-us/dotnet/api/

    run with
        dotnet run
*/

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.IO;

namespace _21
{
    class Program
    {
        static void Main(string[] args)
        {
            var npad = new Keypad(new []{"789", "456", "123", " 0A"});
            var dpad = new Keypad(new []{" ^A", "<v>"});

            ulong p1 = 0, p2 = 0;
            foreach (var code in File.ReadAllLines("input"))
            {
                var numericCode = uint.Parse(code.Substring(0, 3));

                var a = new Robot( 2+1, dpad, npad).MinStepsToType(code);
                var b = new Robot(25+1, dpad, npad).MinStepsToType(code);

                p1 += a * numericCode;
                p2 += b * numericCode;
            }

            Console.WriteLine(p1);
            Console.WriteLine(p2);
        }
    }

    class Robot : IEquatable<Robot>
    {
        Robot controller;
        Keypad keypad;
        Vec2 position;

        class CacheKey : IEquatable<CacheKey>
        {
            Robot robot;
            char button;

            public CacheKey(Robot robot, char button)
            {
                this.robot = robot.Clone();
                this.button = button;
            }

            public bool Equals(CacheKey other)
                => other != null
                && robot.Equals(other.robot)
                && button == other.button;

            public override int GetHashCode()
                => robot.GetHashCode() ^ button.GetHashCode();
        }

        static Dictionary<CacheKey, ulong> cache = new Dictionary<CacheKey, ulong>();

        public Robot() {}

        public Robot(uint controllerCount, Keypad keypad)
        {
            this.keypad = keypad;
            position = keypad.PositionOf('A');
            if (controllerCount > 0)
                controller = new Robot(controllerCount - 1, keypad);
        }

        public Robot(uint controllerCount, Keypad remaining, Keypad initial)
        {
            keypad = initial;
            position = keypad.PositionOf('A');
            if (controllerCount > 0)
                controller = new Robot(controllerCount - 1, remaining);
        }

        public Robot Clone()
        {
            var clone = new Robot();
            clone.keypad = keypad;
            clone.position = position;
            if (controller != null)
                clone.controller = controller.Clone();

            return clone;
        }

        public ulong MinStepsToType(string buttons)
        {
            ulong total = 0;
            foreach (var button in buttons)
                total += MinStepsToType(button);

            return total;
        }

        public ulong MinStepsToType(char button)
        {
            var target = keypad.PositionOf(button);

            var key = new CacheKey(this, button);
            if (Robot.cache.ContainsKey(key)) {
                // no need to move controllers since they're at A
                position = target;
                return Robot.cache[key];
            }

            if (controller == null)
            {
                position = target;
                return 1;
            }

            ulong best = 0;
            Robot bestController = null;
            foreach (var possibility in position.PossibleStepsTo(target))
            {
                var currController = controller.Clone();

                var pos = position;
                ulong total = 0;
                foreach (var step in possibility)
                {
                    pos += step;
                    if (keypad.ButtonAt(pos) == ' ')
                        goto END;

                    total += currController.MinStepsToType(step.ToButton());
                }

                total += currController.MinStepsToType('A');

                if (bestController == null || total < best)
                {
                    best = total;
                    bestController = currController;
                }

                END:;
            }

            position = target;
            controller = bestController;

            Robot.cache[key] = best;

            return best;
        }

        public string ToString(uint depth)
        {
            var result = new String(' ', (int)depth*2) + position.ToString();
            if (controller != null)
                result += $"\n{controller.ToString(depth + 1)}";

            return result;
        }

        public override string ToString()
            => ToString(0);

        public bool Equals(Robot other)
            => other != null
            && position.Equals(other.position)
            && keypad.Equals(other.keypad)
            && (  controller == null && other.controller == null
               || controller != null && controller.Equals(other.controller));

        public override int GetHashCode()
            => position.GetHashCode()
             ^ keypad.GetHashCode()
             ^ (controller != null ? controller.GetHashCode() : 0);
    }

    class Keypad : IEquatable<Keypad>
    {
        Dictionary<Vec2, char> buttons;
        Dictionary<char, Vec2> positions;

        public Keypad(string[] data)
        {
            buttons   = new Dictionary<Vec2, char>();
            positions = new Dictionary<char, Vec2>();

            for (int y=0; y < data.Length; ++y)
            {
                var line = data[y];
                for (int x=0; x < line.Length; ++x)
                {
                    var pos = new Vec2(x, y);
                    var c = line[x];

                    buttons[pos] = c;
                    positions[c] = pos;
                }
            }
        }

        public Vec2 PositionOf(char button)
            => positions[button];

        public char ButtonAt(Vec2 position)
            => buttons[position];

        public bool Equals(Keypad other)
            => other != null
            && buttons.Equals(other.buttons)
            && positions.Equals(other.positions);

        public override int GetHashCode()
            => buttons.GetHashCode() ^ positions.GetHashCode();
    }

    class Vec2 : IEquatable<Vec2>
    {
        public int x { get; }
        public int y { get; }

        public static ImmutableArray<Vec2> directions =
        ImmutableArray.Create<Vec2>(
            new Vec2( 0, -1),  // up
            new Vec2( 1,  0),  // right
            new Vec2( 0,  1),  // down
            new Vec2(-1,  0)   // left
        );

        public Vec2(int x, int y)
        {
            this.x = x;
            this.y = y;
        }

        public uint DistanceTo(Vec2 other)
        {
            // WHY DOES ABS RETURN A SIGNED INTEGER???
            // IT ERRORS ON INT_MIN
            return (uint)Math.Abs(x - other.x) + (uint)Math.Abs(y - other.y);
        }

        public List<List<Vec2>> PossibleStepsTo(Vec2 target)
        {
            var a = new List<Vec2>();
            var b = new List<Vec2>();

            for (int i=x; i < target.x; ++i)
                a.Add(Vec2.directions[1]);
            for (int i=x; i > target.x; --i)
                a.Add(Vec2.directions[3]);
            for (int i=y; i < target.y; ++i) {
                a.Add(Vec2.directions[2]); b.Add(Vec2.directions[2]); }
            for (int i=y; i > target.y; --i) {
                a.Add(Vec2.directions[0]); b.Add(Vec2.directions[0]); }
            for (int i=x; i < target.x; ++i)
                                           b.Add(Vec2.directions[1]);
            for (int i=x; i > target.x; --i)
                                           b.Add(Vec2.directions[3]);

            var possibilities = new List<List<Vec2>>();

            possibilities.Add(a);
            possibilities.Add(b);

            return possibilities;
        }

        public char ToButton()
        {
            if (this.Equals(Vec2.directions[0]))
                return '^';
            if (this.Equals(Vec2.directions[1]))
                return '>';
            if (this.Equals(Vec2.directions[2]))
                return 'v';
            if (this.Equals(Vec2.directions[3]))
                return '<';

            return (char)0;
        }

        public static Vec2 operator +(Vec2 a, Vec2 b)
            => new Vec2(a.x + b.x, a.y + b.y);

        public override string ToString()
            => $"({x}, {y})";

        public bool Equals(Vec2 other)
            => other != null
            && x == other.x
            && y == other.y;

        public override int GetHashCode()
            => y * 9999 + x;
    }
}
