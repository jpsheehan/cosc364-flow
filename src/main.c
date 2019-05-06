#include <stdio.h>
#include <stdlib.h>

struct problem_params_s
{
  int x, y, z;
};

typedef struct problem_params_s ProblemParams;

void print_params(const ProblemParams t_params)
{
  printf("ProblemParams <X=%d, Y=%d, Z=%d>\n", t_params.x, t_params.y, t_params.z);
}

void print_usage(const char *t_program_name)
{
  printf("usage: %s <X> <Y> <Z>\n", t_program_name);
}

int main(int argc, char *argv[])
{
  ProblemParams params;

  if (argc != 4)
  {
    print_usage(argv[0]);
    return EXIT_FAILURE;
  }

  params.x = atoi(argv[1]);
  params.y = atoi(argv[2]);
  params.z = atoi(argv[3]);

  print_params(params);

  return EXIT_SUCCESS;
}