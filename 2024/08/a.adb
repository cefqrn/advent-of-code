--  https://hackaday.com/2024/04/23/programming-ada-first-steps-on-the-desktop/
--  https://learn.adacore.com/courses/intro-to-ada/index.html
--  https://en.wikibooks.org/wiki/Ada_Programming/Libraries/Ada.Containers.Hashed_Sets
--
--  run with
--     gnatmake -o bin/a a.adb -D obj && bin/a
--  in this directory

with Ada.Containers.Hashed_Sets;
with Ada.Containers.Vectors;

with Ada.Text_IO; use Ada.Text_IO;

procedure a is

   type Position is record
      X, Y : Integer;
   end record;

   type Displacement is record
      X, Y : Integer;
   end record;

   function "-" (A, B : Position) return Displacement is
   begin
      return (A.X - B.X, A.Y - B.Y);
   end "-";

   function "+" (P : Position; D : Displacement) return Position is
   begin
      return (P.X + D.X, P.Y + D.Y);
   end "+";


   W, H : Natural := 0;
   function Within_Bounds (P : Position) return Boolean is
   begin
      return 1 <= P.X and P.X <= W
         and 1 <= P.Y and P.Y <= H;
   end Within_Bounds;

   function Hash (P : Position) return Ada.Containers.Hash_Type is
   begin
      return Ada.Containers.Hash_Type (Abs (P.Y * W + P.X));
   end Hash;


   package Position_Sets is new Ada.Containers.Hashed_Sets
     (Element_Type => Position,
      Hash         => Hash,
      Equivalent_Elements => "=");

   package Position_Vectors is new Ada.Containers.Vectors
     (Index_Type   => Positive,
      Element_Type => Position);

   type Antenna is new Character;


   procedure Find_Antinodes
     (Antinodes1, Antinodes2 : in out Position_Sets.Set;
      P : Position;
      D : Displacement) is
   begin
      if Within_Bounds (P + D) and not Antinodes1.Contains(P + D) then
         Antinodes1.Insert (P + D);
      end if;

      declare
         C : Position := P;
      begin
         while Within_Bounds (C) loop
            if not Antinodes2.Contains(C) then
               Antinodes2.Insert (C);
            end if;

            C := C + D;
         end loop;
      end;
   end;


   F : File_Type;
   Antennae : array (Antenna) of Position_Vectors.Vector;
   Antinodes1 : Position_Sets.Set;
   Antinodes2 : Position_Sets.Set;
begin
   Open (F, In_File, "input");
   while not End_Of_File (F) loop
      H := H + 1;
      declare
         Line : String := Get_Line (F);
      begin
         exit when Line'Length = 0;
         W := Line'Length;

         for I in Line'Range loop
            declare
               C : Character := Line (I);
               A : Antenna := Antenna (C);
            begin
               if C /= '.' then
                  Antennae (A).Append ((I, H));
               end if;
            end;
         end loop;
      end;
   end loop;
   Close (F);

   for Frequency of Antennae loop
      for I in Frequency.First_Index .. Frequency.Last_Index loop
         for J in I+1 .. Frequency.Last_Index loop
            declare
               A : Position := Frequency (I);
               B : Position := Frequency (J);
            begin
               Find_Antinodes(Antinodes1, Antinodes2, A, A - B);
               Find_Antinodes(Antinodes1, Antinodes2, B, B - A);
            end;
         end loop;
      end loop;
   end loop;

   Put_Line (Ada.Containers.Count_Type'Image (Position_Sets.Length (Antinodes1)));
   Put_Line (Ada.Containers.Count_Type'Image (Position_Sets.Length (Antinodes2)));
end a;
