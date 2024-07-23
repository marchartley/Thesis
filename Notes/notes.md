# Todo some day :
- My Graph class is using NxN matrices (Adjacency matrix), which is making the access time O(1), but the creation time is O(N^2).
    - Go to a Adjacency list solution instead.

# Thoughts
- The EnvObject "simulation" part is having a complexity of $O(N \times M \times P)$ with $N$ the number of objects, $M$ the "terrain size" (or simulation resolution) and $P$ the number of parameters to take into account.  
The computation is based on the distance to an object, which can be improved using BVH for example, so complexity could be reduced to $O(\log N \times M \times P)$.  
I'm also guessing that the number of environment properties are constant, so the complexity might be $O(M \log N)$  
In any case, this should be very fast using GPGPU.

- The EnvObject "graph" part is impacted by the way graphs are represented. If we consider complete graphs (each object can influence any other), the Adjacency Matrix is probably a better approach; if we consider (non-manifold) meshes (each object affects only the closest objects), the Ajacency List might be better.