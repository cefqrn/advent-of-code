=begin
  https://ruby-doc.org/
  https://learnxinyminutes.com/ruby/
  https://code.golf/wiki/langs/ruby
  https://codegolf.stackexchange.com/questions/363/tips-for-golfing-in-ruby

  run with
    ruby a.rb <input
=end

# initial
# a,_,*b=$<.map &:chomp
# s={""=>1}
# b=b.map &f=->d{s[d]||s[d]=a.split(", ").map{d=~/^#{_1}/?f[$']:0}.sum}
# p b.count{_1>0},b.sum

# 112 by Natte on the code.golf server
# a=gets.scan /\w+/
# c={}
# q=-1
# f=->s{c[s]||=s[1]?a.sum{_1==s[0,l=_1.size]?f[s[l..]]:0}:1}
# p$<.count{q<q+=f[_1]}-1,q

# a,_,*b=$<.map &:chomp
# s={""=>1}
# b=b.map &f=->d{s[d]||=a.split(", ").sum{d=~/^#{_1}/?f[$']:0}}
# p b.count{_1>0},b.sum

# a,_,*b=readlines
# s={$/=>1}
# b=b.map &f=->d{s[d]||=a.scan(/\w+/).sum{d=~/^#{_1}/?f[$']:0}}
# p b.count{_1>0},b.sum

# a,_,*b=$<.map{_1}
# s={$/=>1}
# b=b.map &f=->d{s[d]||=a.scan(/\w+/).sum{d=~/^#{_1}/?f[$']:0}}
# p b.count{_1>0},b.sum

# a=gets.scan /\w+/
# c={"\n"=>1}
# q=-1
# f=->s{c[s]||=a.sum{_1==s[0,l=_1.size]?f[s[l..]]:0}}
# p$<.count{q<q+=f[_1]}-1,q

# a=gets.scan /\w+/
# s={"\n"=>1}
# q=-1
# f=->d{s[d]||=a.sum{d=~/^#{_1}/?f[$']:0}}
# p$<.count{q<q+=f[_1]}-1,q

# a=gets.scan /\w+/
# s={"\n"=>-q=-1}
# f=->d{s[d]||=a.sum{d=~/^#{_1}/?f[$']:0}}
# p$<.count{q<q+=f[_1]}-1,q

# s={gets[-1]=>-q=-1}
# f=->d{s[d]||=$_.scan(/\w+/).sum{d=~/^#{_1}/?f[$']:0}}
# p$<.count{q<q+=f[_1]}-1,q

# gets
# s={$/=>-q=-1}
# f=->d{s[d]||=$_.scan(/\w+/).sum{d=~/^#{_1}/?f[$']:0}}
# p$<.count{q<q+=f[_1]}-1,q

# a=gets
# s={gets=>-~q=0}
# f=->d{s[d]||=a.scan(/\w+/).sum{d=~/^#{_1}/?f[$']:0}}
# p$<.count{q<q+=f[_1]},q

# a=gets.scan /\w+/
# s={$/=>-q=-1}
# f=->d{s[d]||=a.sum{d=~/^#{_1}/?f[$']:0}}
# p$<.count{q<q+=f[_1]}-1,q

# a=gets.scan /\w+/
# s={$/=>-q=-1}
# f=->d{s[d]||=a.sum{d=~/^#{_1}/?f[$']:0}}
# p$<.count{q<q+=f[_1]}-1,q

# a=gets.scan /\w+/
# s={gets=>1}
# b=$<.map &f=->d{s[d]||=a.sum{d=~/^#{_1}/?f[$']:0}}
# p b.count{0<_1},b.sum

# a=gets.scan /\w+/
# s={gets=>1}
# q=0
# f=->d{s[d]||=a.sum{d=~/^#{_1}/?f[$']:0}}
# p$<.count{q<q+=f[_1]},q

# a=gets.scan /\w+/
# s={gets=>1}
# b=$<.map &f=->d{s[d]||=a.sum{d=~/^#{_1}/?f[$']:0}}
# p b.count{_1>0},b.sum

# a=gets.scan /\w+/
# s={gets=>1}
# q=0
# f=->d{s[d]||=a.sum{d=~/^#{_1}/?f[$']:0}}
# p$<.count{q<q+=f[_1]},q

# a=gets.scan /\w+/
# s={gets=>1}
# f=->d{s[d]||=a.sum{d=~/^#{_1}/?f[$']:0}}
# p$<.count{$.<$.+=f[_1]},$.

# a=gets.scan /\w+/
# s={"\n"=>1}
# b=$<.map &f=->d{s[d]||=a.sum{d=~/^#{_1}/?f[$']:0}}
# p $_.count{_1>0}-1,b.sum-1

a=gets.scan /\w+/
s={gets=>q=1}
f=->d{s[d]||=a.sum{d=~/^#{_1}/?f[$']:0}}
p$<.count{q<q+=f[_1]},q-1
