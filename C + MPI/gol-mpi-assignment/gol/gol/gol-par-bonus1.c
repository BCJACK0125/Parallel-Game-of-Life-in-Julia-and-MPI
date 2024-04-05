/***********************

Conway's Game of Life

Based on https://web.cs.dal.ca/~arc/teaching/CS4125/2014winter/Assignment2/Assignment2.html

************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

typedef struct {
   int rows, cols;
   int **cells;
} world;

/* keep short history since we want to detect simple cycles */
#define HISTORY 3

static world worlds[HISTORY];
static int world_iter = 0;
static int world_rows, world_cols;

static world *cur_world;

static int print_cells = 0;
static int print_world = 0;

// use fixed world or random world?

#ifdef FIXED_WORLD
static int random_world = 0;
#else
static int random_world = 1;
#endif

static char *start_world[] = {
    /* Gosper glider gun */
    /* example from https://bitstorm.org/gameoflife/ */
    "..........................................",
    "..........................................",
    "..........................................",
    "..........................................",
    "..........................................",
    "..........................................",
    "........................OO.........OO.....",
    ".......................O.O.........OO.....",
    ".OO.......OO...........OO.................",
    ".OO......O.O..............................",
    ".........OO......OO.......................",
    ".................O.O......................",
    ".................O........................",
    "....................................OO....",
    "....................................O.O...",
    "....................................O.....",
    "..........................................",
    "..........................................",
    ".........................OOO..............",
    ".........................O................",
    "..........................O...............",
    "..........................................",
};

static void
world_init_fixed(world *world)
{
    int **cells = world->cells;
    int row, col;

    /* use predefined start_world */

    for (row = 1; row <= world->rows; row++) {
        for (col = 1; col <= world->cols; col++) {
            if ((row <= sizeof(start_world) / sizeof(char *)) &&
                (col <= strlen(start_world[row - 1]))) {
                cells[row][col] = (start_world[row - 1][col - 1] != '.');
            } else {
                cells[row][col] = 0;
            }
        }
    }
}

static void
world_init_random(world *world)
{
    int **cells = world->cells;
    int row, col;

    // Note that rand() implementation is platform dependent.
    // At least make it reprodible on this platform by means of srand()
    srand(1);

    for (row = 1; row <= world->rows; row++) {
        for (col = 1; col <= world->cols; col++) {
            float x = rand() / ((float)RAND_MAX + 1);
            if (x < 0.5) {
                cells[row][col] = 0;
            } else {
                cells[row][col] = 1;
            }
        }
    }
}

static void
world_print(world *world)
{
    int **cells = world->cells;
    int row, col;

    for (row = 0; row <= world->rows+1; row++) {
        //printf("%d: ", row%10);
        for (col = 1; col <= world->cols; col++) {
            if (cells[row][col]) {
                printf("O");
            } else {
                printf(" ");
            }
        }
        printf("\n");
    }
}

static int
world_count(world *world)
{
    int **cells = world->cells;
    int isum;
    int row, col;

    isum = 0;
    for (row = 1; row <= world->rows; row++) {
        for (col = 1; col <= world->cols; col++) {
            isum = isum + cells[row][col];
        }
    }

    return isum;
}

/* Take world wrap-around into account: */
static void
world_border_wrap(world *world)
{
    int **cells = world->cells;
    int row, col;

    /* left-right boundary conditions */
    for (row = 1; row <= world->rows; row++) {
        cells[row][0] = cells[row][world->cols];
        cells[row][world->cols + 1] = cells[row][1];
    }

    /* top-bottom boundary conditions */
    for (col = 0; col <= world->cols + 1; col++) {
        cells[0][col] = cells[world->rows][col];
        cells[world->rows + 1][col] = cells[1][col];
    }
}

// update board for next timestep
// rows/cols params are the base rows/cols
// excluding the surrounding 1-cell wraparound border
#include <mpi.h>

void world_timestep(  world *old, world *new, int la, int lb, int world_rows, int world_cols )
{
    int **cells = old->cells;
    int row, col;

    //int **matrix = old->cells;

    /* For each element of the matrix apply the */
    /* life game rules                          */
    /* store under temp                         */
    for (row = la; row <= lb; row++) {
        for (col = 1; col <= world_cols; col++) {

            int row_m, row_p, col_m, col_p, nsum;
            int newval;

            // sum surrounding cells
            row_m = row - 1;
            row_p = row + 1;
            col_m = col - 1;
            col_p = col + 1;

            nsum = cells[row_p][col_m] + cells[row_p][col] + cells[row_p][col_p]
                 + cells[row  ][col_m]                     + cells[row  ][col_p]
                 + cells[row_m][col_m] + cells[row_m][col] + cells[row_m][col_p];

            switch (nsum) {
            case 3:
                // a new cell is born
                newval = 1;
                break;
            case 2:
                // the cell, if any, survives
                newval = cells[row][col];
                break;
            default:
                // the cell, if any, dies
                newval = 0;
                break;
            }

            new->cells[row][col] = newval;
        }
    }
}

/* Domain decomposition in strips based on rows */
void decompose_domain( int *start_strip, int *end_strip, int MPIsize, int myrank, int world_rows, int world_cols )
{
    int pe, strip_size;

    start_strip[0] = 1;
    strip_size = ( world_rows ) / ( MPIsize );
    for (  pe=0; pe<MPIsize ; pe++ )
    {
        end_strip[pe] = start_strip[pe] + strip_size - 1;
        if ( pe == MPIsize-1 )
            end_strip[pe] = world_rows;
        else
	        start_strip[pe+1] = end_strip[pe] + 1;
    }
}

void one_line_update(int row, world *old, world *new, int world_cols)
{
    int **cells = old->cells;
    int col;
    for (col = 1; col <= world_cols; col++) {

        int row_m, row_p, col_m, col_p, nsum;
        int newval;

        // sum surrounding cells
        row_m = row - 1;
        row_p = row + 1;
        col_m = col - 1;
        col_p = col + 1;

        nsum = cells[row_p][col_m] + cells[row_p][col] + cells[row_p][col_p]
                + cells[row  ][col_m]                     + cells[row  ][col_p]
                + cells[row_m][col_m] + cells[row_m][col] + cells[row_m][col_p];

        switch (nsum) {
        case 3:
            // a new cell is born
            newval = 1;
            break;
        case 2:
            // the cell, if any, survives
            newval = cells[row][col];
            break;
        default:
            // the cell, if any, dies
            newval = 0;
            break;
        }

        new->cells[row][col] = newval;
    }
}

void new_world_timestep(world *cur_world, world *next_world , int *start_strip, int *end_strip, int myrank, int MPIsize, int world_rows, int world_cols )
{
    int **matrix = cur_world->cells;
    MPI_Status recv_status;
    MPI_Request send_request, recv_request[2];
    int row;
    int la = start_strip[myrank], lb = end_strip[myrank];

    int top_process, bot_process;

    top_process = (myrank+1)%MPIsize;
    bot_process = (MPIsize-1+myrank)%MPIsize;

    MPI_Isend( &matrix[end_strip[myrank]][0], world_cols + 2, MPI_INT, top_process, 102, MPI_COMM_WORLD, &send_request );
    MPI_Isend( &matrix[start_strip[myrank]][0], world_cols + 2, MPI_INT, bot_process, 104, MPI_COMM_WORLD, &send_request );

    MPI_Irecv( &matrix[start_strip[myrank]-1][0], world_cols+2, MPI_INT, bot_process, 102, MPI_COMM_WORLD, &recv_request[0] );
    MPI_Irecv( &matrix[end_strip[myrank]+1][0], world_cols+2, MPI_INT, top_process, 104, MPI_COMM_WORLD, &recv_request[1] );

    for (row = la+1; row <= lb-1; row++) {
        one_line_update(row, cur_world, next_world, world_cols);
    }

    MPI_Wait(&recv_request[0], MPI_STATUS_IGNORE);
    MPI_Wait(&recv_request[1], MPI_STATUS_IGNORE);

    one_line_update(end_strip[myrank], cur_world, next_world, world_cols);
    one_line_update(start_strip[myrank], cur_world, next_world, world_cols);

}

static int
world_check_cycles(int* iter_pin, world *cur_world, int iter, int la, int lb , int world_rows, int world_cols)
{
    int i;

    /* This version re-applies the border wraps so they are consistent with
     * the respective world states, and we can just compare the full world arrays.
     */
    world_border_wrap(cur_world);
    for (i = iter - 1; i >= 0 && i > iter - HISTORY; i--) {
        world *prev_world = &worlds[i % HISTORY];

        int equal = 1;
        for (int i = la; i <= lb; i++) {
            for (int j = 1; j <= world_cols; j++) {
                if (cur_world->cells[i][j] != prev_world->cells[i][j]) {
                    equal = 0;
                    break;
                }
            }
            if (!equal) {
                break;
            }
        }

        if (equal) {
            *iter_pin = i;
            return 1;
        }
    }
    return 0;
}


static int **
alloc_2d_int_array(int nrows, int ncolumns)
{
    int **array;
    int row;

    /* version that keeps the 2d data contiguous, can help caching and slicing across dimensions */
    array = malloc(nrows * sizeof(int *));
    if (array == NULL) {
       fprintf(stderr, "out of memory\n");
       exit(1);
    }

    array[0] = malloc(nrows * ncolumns * sizeof(int));
    if (array[0] == NULL) {
       fprintf(stderr, "out of memory\n");
       exit(1);
    }

    /* memory layout is row-major */
    for (row = 1; row < nrows; row++) {
        array[row] = array[0] + row * ncolumns;
    }

    return array;
}

static double
time_secs(void)
{
    struct timeval tv;
    
    if (gettimeofday(&tv, 0) != 0) {
        fprintf(stderr, "could not do timing\n");
        exit(1);
    }

    return tv.tv_sec + (tv.tv_usec / 1000000.0);
}

int
main(int argc, char *argv[])
{
    int h, nsteps;
    double start_time, end_time, elapsed_time, negative_time = 0.0, t1;
    int i, j;
    int *transfer;
    int *start_strip, *end_strip;
    int pe;
    int ipointer, strip_size, mesg_size, from_strip;
    int terminal_signal = 0, stop_signal = 0, total_stop_signal = 0, iter_pin = 0;

    MPI_Status recv_status;
    
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    /* Get Parameters */
    if (argc != 6) {
        fprintf(stderr, "Usage: %s rows cols steps worldstep cellstep\n", argv[0]);
        exit(1);
    }
    world_rows = atoi(argv[1]);
    world_cols = atoi(argv[2]);
    nsteps = atoi(argv[3]);
    print_world = atoi(argv[4]);
    print_cells = atoi(argv[5]);

    /* initialize worlds, when allocating arrays, add 2 for ghost cells in both directorions */
    for (h = 0; h < HISTORY; h++) {
        worlds[h].rows = world_rows;
        worlds[h].cols = world_cols;
        worlds[h].cells = alloc_2d_int_array(world_rows + 2, world_cols + 2);
    }

    /*  initialize board */
    cur_world = &worlds[world_iter % HISTORY];
    if (random_world) {
        world_init_random(cur_world);
    } else {
        world_init_fixed(cur_world);
    }
    world_border_wrap(cur_world);

    //print the initial world
    if (rank == 0 && print_world > 0) {
        printf("\ninitial world:\n\n");
        world_print(cur_world);
    }

    /* allocate memory for the matrices */
    transfer = (int *)malloc( sizeof(int) * (world_rows + 2) * (world_cols + 2) );

    /* set strip geometry & size*/
    start_strip = (int *)malloc( sizeof(int) * size );
    end_strip = (int *)malloc( sizeof(int) * size );
    decompose_domain( start_strip, end_strip, size, rank, world_rows, world_cols );    

    /*  start timer */ 
    start_time = time_secs();

    /*  time steps */
    for (world_iter = 1; world_iter < nsteps; world_iter++) {
        world *next_world;

        next_world = &worlds[world_iter % HISTORY];

        /* generate a new generation in strip */
        if(size > 1)new_world_timestep( cur_world, next_world, start_strip, end_strip, rank, size, world_rows, world_cols );
        else world_timestep( cur_world, next_world, start_strip[rank], end_strip[rank], world_rows, world_cols );
        /* swap old strip content for new generation */
        cur_world = next_world;


        stop_signal = world_check_cycles(&iter_pin, cur_world, world_iter, start_strip[rank], end_strip[rank], world_rows, world_cols);
        MPI_Allreduce( &stop_signal, &total_stop_signal, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD );

        if ( rank != 0 && ((print_cells>0 || print_world>0) || total_stop_signal == size || world_iter == nsteps-1))
        {
            /* send strip to node 0 */
            ipointer = 0;
            int **matrix = cur_world->cells;
            for( i=start_strip[rank]; i<=end_strip[rank]; i++ )
                for( j = 0 ; j <= world_cols + 1 ; j++ )
                {
                    transfer[ipointer] = matrix[i][j];
                    ipointer++;
                }
            mesg_size = ipointer++;
            MPI_Send( &transfer[0], mesg_size, MPI_INT, 0, 121, MPI_COMM_WORLD );
        }

        /* node 0 */
        if ( rank == 0 )
        {
            t1 = time_secs();
            /* receive content of the strips */
            if((print_cells>0 || print_world>0) || total_stop_signal == size || world_iter == nsteps-1) 
            {
                strip_size = ( world_rows ) / ( size );
                mesg_size = ( world_cols + 2 ) * strip_size;
                for( pe=1; pe <= size-1 ; pe++)
                {
                    MPI_Recv( &transfer[0], mesg_size, MPI_INT, MPI_ANY_SOURCE, 121, MPI_COMM_WORLD, &recv_status );
                    from_strip = recv_status.MPI_SOURCE;
                    ipointer = 0;
                    int **matrix = cur_world->cells;
                    for( i=start_strip[from_strip]; i<= end_strip[from_strip]; i++ )
                    {
                        for( j=0; j<=world_cols+1; j++ )
                        {
                            matrix[i][j] = transfer[ipointer];
                            ipointer++;
                        }
                    }
                }
            }
            t1 = time_secs() - t1;

            if (print_cells > 0 && (world_iter % print_cells) == (print_cells - 1)) {
                printf("%d: %d live cells\n", world_iter, world_count(cur_world));
            }

            if (print_world > 0 && ( (total_stop_signal == size) || (world_iter % print_world) == (print_world - 1))) {
                printf("\nat time step %d:\n\n", world_iter);
                world_print(cur_world);
            }
            
            negative_time += t1;
            

            if (total_stop_signal == size)
            {
                end_time = time_secs();
                elapsed_time = end_time - start_time - negative_time;                
                terminal_signal = 1;

                printf("world iteration %d is equal to iteration %d\n", world_iter, iter_pin);   

                /*  Iterations are done; sum the number of live cells */
                printf("Number of live cells = %d\n", world_count(cur_world));
                fprintf(stderr, "Game of Life took %10.3f seconds\n", elapsed_time);
            }
        }
        MPI_Bcast(&terminal_signal, 1, MPI_INT, 0, MPI_COMM_WORLD);
        if (terminal_signal == 1) 
        {
            break;
        }
    }
    
    if (terminal_signal == 0 && rank == 0)
    {
        end_time = time_secs();
        elapsed_time = end_time - start_time - negative_time;

        /*  Iterations are done; sum the number of live cells */
        printf("Number of live cells = %d\n", world_count(cur_world));
        fprintf(stderr, "Game of Life took %10.3f seconds\n", elapsed_time);
    }

    MPI_Finalize();
    return 0;
}
